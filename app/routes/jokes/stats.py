from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool

from app.core.config import settings
from app.core.rate_limiter import limiter
from app.db.dynamo import get_joke_count
from app.utils.response import success_response

router = APIRouter()

@router.get("/count")
@limiter.limit(settings.RATE_LIMIT_STANDARD)
async def joke_count(request: Request):  # noqa: ARG001
    count = await run_in_threadpool(get_joke_count)

    return success_response({"total_jokes": count})


# This is too expensive to run so hardcoded values it is XD
hardcoded_data = {
    "dad": 147299,
    "short": 231657,
    "yomama": 847,
    "programming": 195,
    "chuck-norris": 527,
    "web-scrape": 5,
    "general": 41,
    "misc": 18,
    "pun": 33,
    "insult": 35
}

@router.get("/countbycategory")
@limiter.limit(settings.RATE_LIMIT_STANDARD)
async def count_by_category(request: Request):  # noqa: ARG001
    return success_response({"total_jokes_by_category": hardcoded_data})
