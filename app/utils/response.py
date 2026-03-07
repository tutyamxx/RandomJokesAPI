from fastapi.responses import JSONResponse

def success_response(data, status_code: int = 200):
    """
    Constructs a standardized JSON success response.

    Args:
        data (Any): The payload to be returned in the 'data' field.
        status_code (int, optional): The HTTP status code. Defaults to 200.

    Returns:
        JSONResponse: A FastAPI response object containing the status and data.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "data": data
        }
    )


def error_response(status_code: int, message: str):
    """
    Constructs a standardized JSON error response.

    Used for returning consistent error structures across the API (e.g., 404, 429, 500).

    Args:
        status_code (int): The HTTP error status code.
        message (str): A human-readable description of the error.

    Returns:
        JSONResponse: A FastAPI response object containing the status and error message.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message
        }
    )
