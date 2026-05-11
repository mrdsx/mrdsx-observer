MAX_RESPONSE_TIME_SECONDS = 20

REPORTS_RETENTION_WINDOW_DAYS = 30
LOGGING_INTERVAL_MINUTES = 5
CACHE_TTL_SECONDS = 60 * (LOGGING_INTERVAL_MINUTES + 1)


class FirestoreKeys:
    PROJECTS_REPORTS = "projects_reports"


class RedisKeys:
    PROJECTS_REPORTS = "projects_reports"

    @staticmethod
    def PROJECT_REPORTS(project_slug: str) -> str:
        return f"{RedisKeys.PROJECTS_REPORTS}:{project_slug}"


project_names = {
    "classic-word-game": "Classic word game",
    "mrdsx-observer": "mrdsx observer",
    "olympiad-preparation": "Olympiad Preparation",
    "swift-tracker": "Swift Tracker",
}
