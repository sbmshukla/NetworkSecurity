from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score, precision_score, recall_score
import sys


def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    """
    Computes precision, recall, and F1 score for classification predictions.
    """
    try:
        logging.info("Calculating classification metrics")

        model_f1 = f1_score(y_true, y_pred)
        model_precision = precision_score(y_true, y_pred)
        model_recall = recall_score(y_true, y_pred)

        logging.info(
            f"F1 Score: {model_f1}, Precision: {model_precision}, Recall: {model_recall}"
        )

        return ClassificationMetricArtifact(
            precision_score=model_precision,
            recall_score=model_recall,
            f1_score=model_f1,
        )

    except Exception as e:
        logging.error(f"Error while calculating classification metrics: {e}")
        raise NetworkSecurityException(e, sys) from e
