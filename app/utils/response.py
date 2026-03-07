from fastapi.responses import JSONResponse

def success_response(data, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "data": data
        }
    )


def error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message
        }
    )
