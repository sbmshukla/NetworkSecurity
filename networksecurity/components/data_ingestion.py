from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

##configuration od data ingestion config

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifacts

import os
import sys
import numpy as np
import pandas as pd
import certifi
import pymongo
from pymongo.mongo_client import MongoClient
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info("Initializing DataIngestion with provided configuration")
            self.data_ingestion_config = data_ingestion_config
            logging.info("DataIngestionConfig successfully loaded")
        except Exception as e:
            logging.error(f"Error during DataIngestion initialization: {e}")
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Read data from MongoDB and convert to DataFrame
        """
        try:
            logging.info("Starting export_collection_as_dataframe")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            logging.info(
                f"Connecting to MongoDB: DB={database_name}, Collection={collection_name}"
            )
            self.mongo_client = MongoClient(MONGO_DB_URL)

            # database_name = "SBMSHUKLA"
            # collection_name = "NetworkDATA"

            collection = self.mongo_client[database_name][collection_name]
            collection_count = collection.count_documents({})

            logging.info(
                f"CountCollection: MongoDB collection contains {collection_count} documents"
            )
            logging.info("Fetching documents from MongoDB collection")

            df = pd.DataFrame(list(collection.find()))
            logging.info(f"Fetched {len(df)} records")

            if df.empty:
                logging.warning(
                    "No data found in MongoDB collection. Skipping ingestion."
                )

            if "_id" in df.columns.to_list():
                logging.info("Dropping '_id' column from DataFrame")
                df = df.drop(columns=["_id"], axis=1)

            logging.info("Replacing 'na' with np.nan")
            df.replace({"na": np.nan}, inplace=True)

            logging.info("DataFrame export completed")
            return df
        except Exception as e:
            logging.error(f"Error in export_collection_as_dataframe: {e}")
            raise NetworkSecurityException(e, sys)

    def export_data_to_feature_store(self, dataframe: pd.DataFrame):
        try:
            logging.info("Starting export_data_to_feature_store")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)

            logging.info(f"Creating directory if not exists: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)

            logging.info(
                f"Saving DataFrame to feature store at: {feature_store_file_path}"
            )
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logging.info("Data successfully saved to feature store")
            return dataframe
        except Exception as e:
            logging.error(f"Error in export_data_to_feature_store: {e}")
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info("Starting split_data_as_train_test")
            logging.info(f"DataFrame contains {len(dataframe)} samples")

            if len(dataframe) < 2:
                msg = f"Insufficient samples ({len(dataframe)}) for train-test split"
                logging.warning(msg)
                raise ValueError(msg)

            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Train-test split successful")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            logging.info(f"Creating directory for train/test files: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)

            logging.info(
                f"Saving training data to: {self.data_ingestion_config.training_file_path}"
            )
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            logging.info("Training file saved")

            logging.info(
                f"Saving testing data to: {self.data_ingestion_config.test_file_path}"
            )
            test_set.to_csv(
                self.data_ingestion_config.test_file_path, index=False, header=True
            )
            logging.info("Testing file saved")
        except Exception as e:
            logging.error(f"Error in split_data_as_train_test: {e}")
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            logging.info("Initiating data ingestion process")

            logging.info("Step 1: Exporting collection as DataFrame")
            dataframe = self.export_collection_as_dataframe()

            logging.info("Step 2: Exporting DataFrame to feature store")
            dataframe = self.export_data_to_feature_store(dataframe=dataframe)

            logging.info("Step 3: Splitting data into train and test sets")
            self.split_data_as_train_test(dataframe=dataframe)

            logging.info("Step 4: Creating DataIngestionArtifacts")
            dataingestionartifact = DataIngestionArtifacts(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.test_file_path,
            )

            logging.info("Data ingestion process completed successfully")
            return dataingestionartifact
        except Exception as e:
            logging.error(f"Error in initiate_data_ingestion: {e}")
            raise NetworkSecurityException(e, sys)
