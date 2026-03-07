from enum import Enum

class APIStatusCode(Enum):
    """
    Enum representing standard API response status codes and labels.

    Each member contains:
        - `code` (int): The HTTP status code to return.
        - `label` (str): A string label representing the status.

    Usage example:
        >>> APIStatusCode.SUCCESS.code
        200
        >>> APIStatusCode.NOT_FOUND.label
        'not_found'

    Members:
        SUCCESS: Standard success response (HTTP 200)
        ERROR: Generic server error response (HTTP 500)
        NOT_FOUND: Resource not found (HTTP 404)
        RATE_LIMIT: Too many requests / rate limited (HTTP 429)
    """
    SUCCESS = (200, "success")
    ERROR = (500, "error")
    NOT_FOUND = (404, "not_found")
    RATE_LIMIT = (429, "rate_limit")

    def __init__(self, code: int, label: str):
        self.code = code
        self.label = label
