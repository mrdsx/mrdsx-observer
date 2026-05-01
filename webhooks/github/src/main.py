from typing import Annotated, Any

from fastapi import BackgroundTasks, FastAPI, Header

from src.services import deploy_app

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.post("/webhook")
def read_webhook(
    event_payload: dict[str, Any],
    x_github_event: Annotated[str | None, Header()],
    bg_tasks: BackgroundTasks,
):
    ref = event_payload.get("ref")
    if ref is None:
        return {"status": "ok"}

    if x_github_event == "push" and ref == "refs/heads/main":
        bg_tasks.add_task(deploy_app)

    return {"status": "ok"}
