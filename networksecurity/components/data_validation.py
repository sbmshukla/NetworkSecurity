from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifacts,
    DataValidationArtifacts,
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH, TRAIN_FILE_NAME
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifacts,
        data_validation_config: DataValidationConfig,
    ):
        try:
            logging.info("Initializing DataValidation class.")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            logging.info("Schema file loaded successfully.")
        except Exception as e:
            logging.error("Error during DataValidation initialization.")
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Failed to read data from {file_path}")
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"DataFrame has columns: {len(dataframe.columns)}")

            if len(dataframe.columns) == number_of_columns:
                logging.info("Column count validation passed.")
                return True
            logging.warning("Column count validation failed.")
            return False
        except Exception as e:
            logging.error("Error during column count validation.")
            raise NetworkSecurityException(e, sys)

    def validate_numeric_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = self._schema_config.get("numerical_columns", [])
            logging.info(f"Validating numerical columns: {numerical_columns}")

            for col in numerical_columns:
                if col not in dataframe.columns:
                    logging.error(f"Missing column: {col}")
                    raise NetworkSecurityException(f"Missing column: {col}", sys)
                if not pd.api.types.is_numeric_dtype(dataframe[col]):
                    logging.error(f"Non-numeric column: {col}")
                    raise NetworkSecurityException(f"Non-numeric column: {col}", sys)

            logging.info("Numeric column validation passed.")
            return True

        except Exception as e:
            logging.error("Error during numeric column validation.")
            raise NetworkSecurityException(f"Validation failed: {str(e)}", sys)

    def detect_dataset_drifts(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)

                if threshold < is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update(
                    {
                        column: {
                            "p_value": float(is_same_dist.pvalue),
                            "drift_status": is_found,
                        }
                    }
                )

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            ## create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            logging.info("Starting data validation process.")

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            logging.info("Validating number of columns in train DataFrame.")
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = "Train dataframe does not contains all columns.\n"
                logging.error(error_message)

            logging.info("Validating number of columns in test DataFrame.")
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = "Test dataframe does not contains all columns.\n"
                logging.error(error_message)

            logging.info("Validating numeric columns in train DataFrame.")
            status = self.validate_numeric_columns(dataframe=train_dataframe)
            if not status:
                error_message = (
                    "Train dataframe does not contains valid numeric columns.\n"
                )
                logging.error(error_message)

            logging.info("Validating numeric columns in test DataFrame.")
            status = self.validate_numeric_columns(dataframe=test_dataframe)
            if not status:
                error_message = (
                    "Test dataframe does not contains valid numeric columns.\n"
                )
                logging.error(error_message)

            ## lets check datadrifts
            status = self.detect_dataset_drifts(
                base_df=train_dataframe, current_df=test_dataframe
            )

            dir_path = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            data_validation_artifacts = DataValidationArtifacts(
                validation_satus=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            return data_validation_artifacts

        except Exception as e:
            logging.error("Data validation failed.")
            raise NetworkSecurityException(e, sys)
