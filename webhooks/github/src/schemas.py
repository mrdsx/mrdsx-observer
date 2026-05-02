from pydantic import BaseModel


class GithubCommit(BaseModel):
    added: list[str]
    removed: list[str]
    modified: list[str]


class GithubWebhookEvent(BaseModel):
    ref: str
    forced: bool
    commits: list[GithubCommit]
