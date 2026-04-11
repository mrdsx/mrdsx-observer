from functools import lru_cache

from firebase_admin.firestore_async import client as create_async_firestore
from redis.asyncio import Redis

from repositories.projects_reports import ProjectsReportsRepository
from services.projects_reports import ProjectsReportsService
from src.core.firebase.types import AsyncFirestore
from src.core.settings import get_settings

settings = get_settings()


@lru_cache
def get_firestore() -> AsyncFirestore:
    return create_async_firestore()


@lru_cache
def get_redis() -> Redis:
    return Redis(**settings.redis_settings)


def get_projects_reports_service() -> ProjectsReportsService:
    return ProjectsReportsService()


def get_projects_reports_repository() -> ProjectsReportsRepository:
    return ProjectsReportsRepository()
