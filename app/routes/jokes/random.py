from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.rate_limiter import limiter
from app.core.status_codes import APIStatusCode
from app.db.dynamo import get_random_joke, get_random_ten_jokes
from app.utils.response import error_response, success_response

router = APIRouter()

@router.get("/random")
@limiter.limit(settings.RATE_LIMIT_STANDARD)
async def random_joke(request: Request):
    joke = get_random_joke()

    if not joke:
        return error_response(APIStatusCode.NOT_FOUND.code, "No jokes found")

    return success_response(joke)

@router.get("/random/ten")
@limiter.limit(settings.RATE_LIMIT_STANDARD)
async def random_ten_jokes(request: Request):
    jokes = get_random_ten_jokes()

    if not jokes:
        return error_response(APIStatusCode.NOT_FOUND.code, "Could not retrieve random jokes")

    return success_response(jokes)
