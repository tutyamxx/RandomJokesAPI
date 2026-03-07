from fastapi import APIRouter

from .random import router as random_router
from .search import router as search_router
from .stats import router as stats_router

jokes_router = APIRouter(prefix="/jokes", tags=["Jokes"])

jokes_router.include_router(stats_router)
jokes_router.include_router(random_router)
jokes_router.include_router(search_router)
