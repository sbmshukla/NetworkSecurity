from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import f1_score
import yaml
import os, sys
import numpy as np
import dill
import pickle


def read_yaml_file(file_path: str) -> dict:
    """Load and return YAML content from a file."""
    try:
        with open(file_path, "rb") as yaml_file:
            content = yaml.safe_load(yaml_file)
        logging.info("YAML file read successfully")
        return content
    except Exception as e:
        logging.error(f"Failed to read YAML: {e}")
        raise NetworkSecurityException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """Write content to a YAML file, replacing if needed."""
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Replaced existing file: {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
        logging.info("YAML file written successfully")
    except Exception as e:
        logging.error(f"Failed to write YAML: {e}")
        raise NetworkSecurityException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """Save a NumPy array to a binary .npy file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
        logging.info("NumPy array saved successfully")
    except Exception as e:
        logging.error(f"Failed to save NumPy array: {e}")
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path, obj: object) -> None:
    """Serialize and save a Python object using pickle."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Object saved successfully")
    except Exception as e:
        logging.error(f"Failed to save object: {e}")
        raise NetworkSecurityException(e, sys) from e


def load_object(file_path) -> object:
    """
    Loading Saved Object From Given Path & Returning It.
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The File: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    Loding Saved Numpy Array From Give Path & Returning It.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def evaluate_model(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}

        for model_name, model in models.items():
            logging.info(f"Starting evaluation for model: {model_name}")

            cv = StratifiedKFold(n_splits=3, shuffle=False)
            logging.info(
                f"Performing GridSearchCV for {model_name} with parameters: {params[model_name]}"
            )
            gs = GridSearchCV(estimator=model, param_grid=params[model_name], cv=cv)
            gs.fit(X_train, y_train)

            logging.info(f"Best parameters for {model_name}: {gs.best_params_}")
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            logging.info(f"Model {model_name} trained with best parameters")

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = f1_score(y_train, y_train_pred)
            test_model_score = f1_score(y_test, y_test_pred)

            logging.info(
                f"{model_name} F1 Score - Train: {train_model_score:.4f}, Test: {test_model_score:.4f}"
            )
            report[model_name] = test_model_score

        logging.info("Model evaluation completed successfully")
        return report

    except Exception as e:
        logging.error(f"Error during model evaluation: {e}")
        raise NetworkSecurityException(e, sys) from e
