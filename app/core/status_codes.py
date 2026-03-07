from enum import Enum

class APIStatusCode(Enum):
    SUCCESS = (200, "success")
    ERROR = (500, "error")
    NOT_FOUND = (404, "not_found")
    RATE_LIMIT = (429, "rate_limit")

    def __init__(self, code: int, label: str):
        self.code = code
        self.label = label
