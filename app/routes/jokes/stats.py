from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.rate_limiter import limiter
from app.db.dynamo import get_joke_count
from app.utils.response import success_response

router = APIRouter()

@router.get("/count")
@limiter.limit(settings.RATE_LIMIT_STANDARD)
async def joke_count(request: Request):
    count = get_joke_count()

    return success_response({"total_jokes": count})
