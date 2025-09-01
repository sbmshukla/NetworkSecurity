import sys


class NetworkSecurityException(Exception):
    """
    Custom exception for network security tools.
    Captures filename and line number where the error occurred for better traceability.
    """

    def __init__(self, error_message: str, error_details: sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return (
            f"Error occurred in Python script: '{self.file_name}', "
            f"line {self.lineno}. Message: {self.error_message}"
        )
