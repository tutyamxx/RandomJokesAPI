from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.rate_limiter import init_limiter
from app.core.status_codes import APIStatusCode
from app.routes.jokes import jokes_router
from app.utils.middleware import init_middleware
from app.utils.response import error_response

print("🐍 FastAPI app loaded, handler ready")  # noqa: T201

# Base directory (safe for serverless)
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="RandomJokesAPI")

# Setup middleware
init_middleware(app)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialize limiter
limiter = init_limiter(app)
print(f"🐌 [RateLimiter] Using rate limit: {settings.RATE_LIMIT_STANDARD}")  # noqa: T201

# Rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return error_response(APIStatusCode.RATE_LIMIT.code, "Too many requests. Slow down!")

# Validation error handler (Handles invalid UUIDs and malformed inputs)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_data = error_response(APIStatusCode.INVALID_PARAMETER.code, "Invalid input format. Please ensure your UUID is correct.")

    return error_data

# Favicon route
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(STATIC_DIR / "favicon.ico")


# Root route
@app.get("/")
async def root():
    return JSONResponse(
        status_code=APIStatusCode.SUCCESS.code,
        content={
            "status": APIStatusCode.SUCCESS.code,
            "data": {
                "message": "🤡 RandomJokesAPI is running.",
                "endpoints": {
                    "random_joke": "/jokes/random",
                    "random_10_jokes": "/jokes/random/ten",
                    "total_jokes": "/jokes/count",
                    "joke_by_id": "/jokes/{joke_id}",
                    "jokes_by_category": "/jokes/category/{category}",
                    "total_jokes_by_category": "/jokes/countbycategory"
                }
            }
        }
    )


# Include routers
app.include_router(jokes_router)
