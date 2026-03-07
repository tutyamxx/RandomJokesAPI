from fastapi import APIRouter, Request

from app.db.dynamo import get_random_joke, get_joke_by_id, get_jokes_by_category

from app.core.status_codes import APIStatusCode
from app.core.config import settings
from app.core.rate_limiter import limiter

from app.utils.response import success_response, error_response

router = APIRouter(prefix="/jokes")

# Routes
@router.get("/random")
@limiter.limit(settings.RATE_LIMIT)
async def random_joke(request: Request):
    joke = get_random_joke()

    if not joke:
        return error_response(APIStatusCode.NOT_FOUND.code, "No jokes found")

    return success_response(joke)


@router.get("/{joke_id}")
@limiter.limit(settings.RATE_LIMIT)
async def joke_by_id(joke_id: str, request: Request):
    joke = get_joke_by_id(joke_id)

    if not joke:
        return error_response(APIStatusCode.NOT_FOUND.code, "Joke not found")

    return success_response(joke)


@router.get("/category/{category}")
@limiter.limit(settings.RATE_LIMIT)
async def jokes_category(category: str, request: Request):
    items = get_jokes_by_category(category)

    if not items:
        return error_response(APIStatusCode.NOT_FOUND.code, "No jokes found in this category")

    return success_response(items)
