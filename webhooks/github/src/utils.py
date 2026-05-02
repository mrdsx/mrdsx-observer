import os
import subprocess

from src.schemas import GithubCommit, GithubWebhookEvent
from src.settings import settings

START_SERVICE_SCRIPT = f"./start-service.{settings.app_env}.sh"


def deploy_app(github_event: GithubWebhookEvent) -> None:
    if github_event.forced:
        print("Skipping deployment due to forced push.")
        return

    services = get_services_from_commits(github_event.commits)
    handle_services_start(services)


def get_services_from_commits(commits: list[GithubCommit]) -> set[str]:
    services = set([])

    for commit in commits:
        services.update(get_services_from_paths(commit.added))
        services.update(get_services_from_paths(commit.modified))
        services.update(get_services_from_paths(commit.removed))

    return services


def get_services_from_paths(paths: list[str]) -> set[str]:
    services = set([])

    for path in paths:
        if path.startswith("frontend/"):
            services.add("frontend")
        if path.startswith("backend/"):
            services.add("backend")

    return services


def handle_services_start(services: set[str]) -> None:
    os.chdir("../../scripts")
    subprocess.run(["chmod", "+x", START_SERVICE_SCRIPT])
    for service in services:
        subprocess.Popen(
            [
                "flock",
                "-n",
                f"/tmp/start-{service}.lock",
                "-c",
                f"{START_SERVICE_SCRIPT} {service}",
            ]
        )
    os.chdir("../webhooks/github")
