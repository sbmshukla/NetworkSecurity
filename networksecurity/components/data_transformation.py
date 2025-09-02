from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import (
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
)

from networksecurity.entity.artifact_entity import (
    DataValidationArtifacts,
    DataTransformationArtifacts,
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object
import os
import sys
import numpy as np
import pandas as pd


from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline


class DataTransformation:

    def __init__(
        self,
        data_validation_artifacts: DataValidationArtifacts,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifacts: DataValidationArtifacts = (
                data_validation_artifacts
            )
            self.data_transformation_config: DataTransformationConfig = (
                data_transformation_config
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(cls) -> Pipeline:
        logging.info(
            "Entered get_data_transformer_object method of transformation class"
        )
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor: Pipeline = Pipeline(steps=[("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def intiate_data_transformation(self) -> DataTransformationArtifacts:
        logging.info("Entered the intiate_data_transformation method")
        try:
            logging.info("Starting data transformation")

            train_df: pd.DataFrame = DataTransformation.read_data(
                self.data_validation_artifacts.valid_train_file_path
            )
            test_df: pd.DataFrame = DataTransformation.read_data(
                self.data_validation_artifacts.valid_test_file_path
            )

            ## training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            ## testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()

            logging.info(f"XYZ: {preprocessor}")

            preprocessor_obj = preprocessor.fit(input_feature_train_df)

            transformed_input_train_feature = preprocessor_obj.transform(
                input_feature_train_df
            )

            transformed_input_test_feature = preprocessor_obj.transform(
                input_feature_test_df
            )

            train_arr = np.c_[
                transformed_input_train_feature, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                transformed_input_test_feature, np.array(target_feature_test_df)
            ]

            ## save numpy array data
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                obj=preprocessor_obj,
            )

            save_object("final_model/preprocessor.pkl", preprocessor_obj)
            ## preparing artifacts

            dataclass_transform_artifacts = DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return dataclass_transform_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)
