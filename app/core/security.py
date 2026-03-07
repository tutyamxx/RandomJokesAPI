import os
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        is_production = os.getenv("ENV") == "production"

        # Modern Browser Isolation & Resource Control
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Origin-Agent-Cluster"] = "?1"

        # Legacy & Specific Compatibility
        response.headers["X-DNS-Prefetch-Control"] = "off"
        response.headers["X-Download-Options"] = "noopen"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        # Disabling legacy XSS protection as it can create more vulnerabilities than it solves in modern browsers.
        response.headers["X-XSS-Protection"] = "0"

        # Core Protections (Always On)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Remove X-Powered-By if present to hide server signature
        if "X-Powered-By" in response.headers:
            del response.headers["X-Powered-By"]

        # Permissions Policy (Restrict hardware access)
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Production-Only Hardening
        if is_production:
            # Force HTTPS for 1 year
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

            # Strict Content Security Policy
            # Note: default-src 'self' is quite restrictive. Ensure assets are local.
            response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none';"
        else:
            # CSP for local Swagger UI / Redoc testing
            response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline';"

        return response
