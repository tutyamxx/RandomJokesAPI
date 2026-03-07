from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes.jokes import router as jokes_router

from app.core.security import SecurityHeadersMiddleware
from app.core.rate_limiter import init_limiter
from app.core.status_codes import APIStatusCode
from app.core.config import settings

from slowapi.errors import RateLimitExceeded

from app.utils.response import error_response

app = FastAPI(title="RandomJokesAPI")

# Initialize limiter & middleware
limiter = init_limiter(app)
print(f"🐌 [RateLimiter] Using rate limit: {settings.RATE_LIMIT}")

# Exception handler for rate limits
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return error_response(APIStatusCode.RATE_LIMIT.code, "Too many requests. Slow down!")

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    return JSONResponse(
        status_code=APIStatusCode.SUCCESS.code,
        content={
            "status": APIStatusCode.SUCCESS.code,
            "data": {
                "message": "Jokes API is running.",
                "endpoints": {
                    "random_joke": "/jokes/random",
                    "joke_by_id": "/jokes/{joke_id}",
                    "jokes_by_category": "/jokes/category/{category}"
                }
            }
        }
    )

# Include jokes router
app.include_router(jokes_router)