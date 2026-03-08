from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.security import SecurityHeadersMiddleware


def init_middleware(app: FastAPI):
    """
    Registers all middleware for the application.
    """

    # This first - Custom Security Headers
    app.add_middleware(SecurityHeadersMiddleware)

    # This second - CORS Configuration
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["GET"], allow_headers=["*"])

    # This last
    # Processes the response last (outermost layer) to compress the final output
    # Only compress responses larger than 1KB with Balanced CPU vs Compression ratio
    app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)
