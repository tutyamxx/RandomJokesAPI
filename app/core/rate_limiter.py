from slowapi import Limiter
from slowapi.util import get_remote_address


# Log client IPs for debugging
def get_remote_address_with_log(request):
    """
    Retrieve the remote IP address from a request and log it.

    This function wraps `slowapi.util.get_remote_address` and prints
    a message to the console for debugging or monitoring purposes.

    Args:
        request (starlette.requests.Request): The incoming HTTP request object.

    Returns:
        str: The IP address of the client making the request.
    """
    addr = get_remote_address(request)
    print("🐌 [RateLimiter] Request from", format(addr))  # noqa: T201

    return addr


limiter = Limiter(key_func=get_remote_address_with_log, enabled=True)

def init_limiter(app):
    """
    Initialize SlowAPI rate limiting for a FastAPI application.

    This function sets the limiter instance in the application's state
    and adds the `SlowAPIMiddleware` to enable rate limiting on routes.

    Args:
        app (fastapi.FastAPI): The FastAPI application instance.

    Returns:
        Limiter: The initialized SlowAPI Limiter instance.
    """
    app.state.limiter = limiter

    from slowapi.middleware import SlowAPIMiddleware
    app.add_middleware(SlowAPIMiddleware)

    return limiter
