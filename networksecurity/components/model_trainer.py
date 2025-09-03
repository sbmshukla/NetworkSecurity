from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifacts,
    ModelTrainerArtifact,
)
from networksecurity.entity.config_entity import ModelTrainerConfig

import os
import sys

from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_model,
)
from networksecurity.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow

# import dagshub

# dagshub.init(repo_owner="sbmshukla", repo_name="NetworkSecurity", mlflow=True)


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifacts: DataTransformationArtifacts,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifacts = data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, best_model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            mlflow.sklearn.log_model(best_model, "model")

            # mlflow.sklearn.log_model(
            #     sk_model=best_model,
            #     name="network_security_model",  # ✅ lowercase, valid characters
            #     registered_model_name="network_security_model",  # ✅ matches name
            # )

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Logistic Regression": LogisticRegression(verbose=1),
            # "K-Nearest Neighbors": KNeighborsClassifier(),  # No verbose param
            # "Decision Tree": DecisionTreeClassifier(),  # No verbose param
            # "Random Forest": RandomForestClassifier(verbose=1),
            # "AdaBoost": AdaBoostClassifier(),  # No verbose param
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
        }

        params = {
            "Logistic Regression": {
                # "penalty": ["l1", "l2", "elasticnet", None],
                # "solver": ["liblinear", "saga"],
                # "C": [0.01, 0.1, 1, 10],
                "max_iter": [100, 500, 1000],
            },
            "K-Nearest Neighbors": {
                "n_neighbors": [3, 5, 7, 9],
                # "weights": ["uniform", "distance"],
                "metric": ["euclidean", "manhattan"],
            },
            "Decision Tree": {
                "criterion": ["gini", "entropy"],
                # "max_depth": [None, 5, 10, 20],
                # "min_samples_split": [2, 5, 10],
                # "min_samples_leaf": [1, 2, 4],
            },
            "Random Forest": {
                "n_estimators": [50, 100, 200],
                # "max_depth": [None, 10, 20],
                # "min_samples_split": [2, 5],
                # "min_samples_leaf": [1, 2],
                # "bootstrap": [True, False],
            },
            "AdaBoost": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 1],
                # "algorithm": ["SAMME", "SAMME.R"],
            },
            "Gradient Boosting": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 0.2],
                # "max_depth": [3, 5, 10],
                "subsample": [0.6, 0.8, 1.0],
            },
        }

        model_report: dict = evaluate_model(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models=models,
            params=params,
        )

        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        logging.info(
            f"Best Model {best_model_name} | Best Model Score: {best_model_score}"
        )

        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(
            y_true=y_train, y_pred=y_train_pred
        )

        ## Track The Experiment With MlFlow
        self.track_mlflow(best_model, classification_train_metric)

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(
            y_true=y_test, y_pred=y_test_pred
        )

        ## Track The Experiment With MlFlow
        self.track_mlflow(best_model, classification_test_metric)

        preprocessor = load_object(
            file_path=self.data_transformation_artifacts.transformed_object_file_path
        )
        model_dir_path = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )
        os.makedirs(model_dir_path, exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(
            self.model_trainer_config.trained_model_file_path, obj=Network_Model
        )

        save_object("final_model/model.pkl", best_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_matric_artifact=classification_test_metric,
        )

        logging.info(model_trainer_artifact)

        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = (
                self.data_transformation_artifacts.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifacts.transformed_test_file_path
            )

            ## loading training and testing data
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact = self.train_model(X_train, y_train, X_test, y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
