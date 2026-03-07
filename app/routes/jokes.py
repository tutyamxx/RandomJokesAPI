from uuid import UUID

from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.rate_limiter import limiter
from app.core.status_codes import APIStatusCode
from app.db.dynamo import (
    get_joke_by_id,
    get_joke_count,
    get_jokes_by_category,
    get_random_joke,
    get_random_ten_jokes,
)
from app.utils.response import error_response, success_response

router = APIRouter(prefix="/jokes")

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
        return error_response(
            APIStatusCode.NOT_FOUND.code,
            "Could not retrieve random jokes"
        )

    return success_response(jokes)

@router.get("/count")
@limiter.limit(settings.RATE_LIMIT_STANDARD)
async def joke_count(request: Request):
    count = get_joke_count()

    return success_response({"total_jokes": count})

@router.get("/{joke_id}")
@limiter.limit(settings.RATE_LIMIT_STANDARD)
async def joke_by_id(joke_id: UUID, request: Request):
    joke = get_joke_by_id(str(joke_id))

    if not joke:
        return error_response(APIStatusCode.NOT_FOUND.code, "Joke not found")

    return success_response(joke)

@router.get("/category/{category}")
@limiter.limit(settings.RATE_LIMIT_SEARCH)
async def jokes_category(category: str, request: Request):
    items = get_jokes_by_category(category)

    if not items:
        return error_response(
            APIStatusCode.NOT_FOUND.code,
            f"No jokes found in category: {category}"
        )

    return success_response(items)
