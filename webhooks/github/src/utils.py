import os
import subprocess

from src.schemas import GithubCommit, GithubWebhookEvent
from src.settings import settings

START_SERVICE_SCRIPT = f"./start-service.{settings.app_env}.sh"
SYNC_CODE_SCRIPT = "./sync-code.sh"


def deploy_app(github_event: GithubWebhookEvent) -> None:
    if github_event.forced:
        print("Skipping deployment due to forced push.")
        return

    services = get_services_from_commits(github_event.commits)
    handle_services_start(services)
    handle_webhooks_update(github_event.commits)


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


def handle_webhooks_update(commits: list[GithubCommit]) -> None:
    os.chdir("../../scripts")
    any_updated = any_webhook_updated(commits)
    if any_updated:
        subprocess.run(["chmod", "+x", SYNC_CODE_SCRIPT])
        subprocess.Popen([SYNC_CODE_SCRIPT])
    os.chdir("../webhooks/github")


def any_webhook_updated(commits: list[GithubCommit]) -> bool:
    for commit in commits:
        for added in commit.added:
            if added.startswith("webhooks/"):
                return True

        for removed in commit.removed:
            if removed.startswith("webhooks/"):
                return True

        for modified in commit.modified:
            if modified.startswith("webhooks/"):
                return True

    return False


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
