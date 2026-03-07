from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool

from app.core.config import settings
from app.core.rate_limiter import limiter
from app.core.status_codes import APIStatusCode
from app.db.dynamo import get_joke_by_id, get_jokes_by_category
from app.utils.response import error_response, success_response

router = APIRouter()

@router.get("/{joke_id}")
@limiter.limit(settings.RATE_LIMIT_STANDARD)
async def joke_by_id(joke_id: UUID, request: Request):
    joke = await run_in_threadpool(get_joke_by_id, str(joke_id))

    if not joke:
        return error_response(APIStatusCode.NOT_FOUND.code, "Joke not found")

    return success_response(joke)

@router.get("/category/{category}")
@limiter.limit(settings.RATE_LIMIT_SEARCH)
async def jokes_category(category: str, request: Request):
    items = await run_in_threadpool(get_jokes_by_category, category)

    if not items:
        return error_response(
            APIStatusCode.NOT_FOUND.code,
            f"No jokes found in category: {category}"
        )

    return success_response(items)
