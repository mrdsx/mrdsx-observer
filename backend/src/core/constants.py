MAX_RESPONSE_TIME_SECONDS = 20

REPORTS_RETENTION_WINDOW_DAYS = 30
LOGGING_INTERVAL_MINUTES = 5
CACHE_TTL_SECONDS = 60 * (LOGGING_INTERVAL_MINUTES + 1)


class RedisKeys:
    PROJECTS_REPORTS = "projects_reports"


project_names = {
    "classic-word-game": "Classic word game",
    "olympiad-preparation": "Olympiad Preparation",
    "swift-tracker": "Swift Tracker",
}
