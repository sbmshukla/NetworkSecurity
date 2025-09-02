from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    TrainingPipelineConfig,
)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info("Starting Training Pipeline Configuration")
        training_pipeline_config = TrainingPipelineConfig()

        logging.info("Creating Data Ingestion Configuration")
        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )

        logging.info("Initializing Data Ingestion Component")
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)

        logging.info("Initiating Data Ingestion Process")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion Completed. Artifact: {data_ingestion_artifact}")

        logging.info("Creating Data Validation Configuration")
        data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config
        )

        logging.info("Initializing Data Validation Component")
        datavalidation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config,
        )

        logging.info("Initiating Data Validation Process")
        data_validation_artifact = datavalidation.initiate_data_validation()
        logging.info(f"Data Validation Completed. Artifact: {data_validation_artifact}")

        print("Pipeline execution completed successfully.")

    except Exception as e:
        logging.error("Exception occurred during pipeline execution", exc_info=True)
        raise NetworkSecurityException(e, sys)
