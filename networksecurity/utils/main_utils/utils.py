from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
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
        raise NetworkSecurityException(e, sys)


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
        raise NetworkSecurityException(e, sys)


def save_numpy_array_data(file_path: str, array: np.array):
    """Save a NumPy array to a binary .npy file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
        logging.info("NumPy array saved successfully")
    except Exception as e:
        logging.error(f"Failed to save NumPy array: {e}")
        raise NetworkSecurityException(e, sys)


def save_object(file_path, obj: object) -> None:
    """Serialize and save a Python object using pickle."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Object saved successfully")
    except Exception as e:
        logging.error(f"Failed to save object: {e}")
        raise NetworkSecurityException(e, sys)
