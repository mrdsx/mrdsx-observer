from src.core.settings import get_settings
from src.repositories.projects_reports import ProjectsReportsRepository
from src.services.projects_reports import ProjectsReportsService
from src.services.services_reports import ServicesReportsService

settings = get_settings()


def get_projects_reports_service() -> ProjectsReportsService:
    return ProjectsReportsService()


def get_projects_reports_repository() -> ProjectsReportsRepository:
    return ProjectsReportsRepository()


def get_services_reports_service() -> ServicesReportsService:
    return ServicesReportsService()
