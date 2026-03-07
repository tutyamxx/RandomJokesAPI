import os
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        is_production = os.getenv("ENV") == "production"

        # Core Protections (Always On)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy (Restrict hardware access)
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Production-Only Hardening
        if is_production:
            # Force HTTPS for 1 year
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

            # Strict Content Security Policy
            response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'none'; object-src 'none';"
        else:
            # CSP for local Swagger UI / Redoc testing
            response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline';"

        return response
