from typing import Annotated

from fastapi import BackgroundTasks, Body, FastAPI, Header, Request

from src.lifespan import lifespan
from src.schemas import GithubWebhookEvent
from src.settings import settings
from src.utils import deploy_app
from src.validation import verify_signature

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhook")
async def read_webhook(
    github_event: Annotated[GithubWebhookEvent, Body()],
    x_github_event: Annotated[str, Header()],
    x_hub_signature_256: Annotated[str, Header()],
    request: Request,
    bg_tasks: BackgroundTasks,
) -> dict[str, str]:
    payload = await request.body()
    verify_signature(settings.webhook_secret, payload, x_hub_signature_256)

    if x_github_event == "push" and github_event.ref == "refs/heads/main":
        bg_tasks.add_task(deploy_app, github_event=github_event)

    return {"status": "ok"}
