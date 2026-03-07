from slowapi import Limiter
from slowapi.util import get_remote_address

# Log client IPs for debugging
def get_remote_address_with_log(request):
    addr = get_remote_address(request)
    print(f"🐌 [RateLimiter] Request from {addr}")

    return addr

limiter = Limiter(key_func=get_remote_address_with_log, enabled=True)

def init_limiter(app):
    app.state.limiter = limiter

    from slowapi.middleware import SlowAPIMiddleware
    app.add_middleware(SlowAPIMiddleware)

    return limiter
