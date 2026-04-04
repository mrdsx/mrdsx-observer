from fastapi import APIRouter
from .projects_router import router as projects_router


api_router = APIRouter(prefix="/api")
api_router.include_router(projects_router)

__all__ = ["api_router"]
