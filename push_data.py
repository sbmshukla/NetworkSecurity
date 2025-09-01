import json
import os
import sys
import pandas as pd
import pymongo
import certifi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logging.info(f"Converted {len(records)} records from CSV to JSON")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongo(self, records, database_name, collection_name):
        try:
            db = self.mongo_client[database_name]
            collection = db[collection_name]
            result = collection.insert_many(records)
            logging.info(
                f"Inserted {len(result.inserted_ids)} records into {database_name}.{collection_name}"
            )
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        FILE_PATH = "Network_Data/phisingData.csv"
        DATABASE_NAME = "SBMSHUKLA"
        COLLECTION_NAME = "NetworkDATA"

        extractor = NetworkDataExtract()
        records = extractor.csv_to_json_convertor(file_path=FILE_PATH)
        inserted_count = extractor.insert_data_to_mongo(
            records=records,
            database_name=DATABASE_NAME,
            collection_name=COLLECTION_NAME,
        )
        print(f"Successfully inserted {inserted_count} records.")
    except Exception as e:
        logging.error(f"Failed to insert data: {e}")
