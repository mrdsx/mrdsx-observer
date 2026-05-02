from typing import Annotated

from fastapi import BackgroundTasks, FastAPI, Header

from src.schemas import GithubWebhookEvent
from src.utils import deploy_app

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhook")
def read_webhook(
    github_event: GithubWebhookEvent,
    x_github_event: Annotated[str | None, Header()],
    bg_tasks: BackgroundTasks,
) -> dict[str, str]:
    if x_github_event == "push" and github_event.ref == "refs/heads/main":
        bg_tasks.add_task(deploy_app, github_event=github_event)

    return {"status": "ok"}
