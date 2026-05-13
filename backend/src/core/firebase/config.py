import json

from src.core.settings import get_settings

settings = get_settings()

with open("./src/service_account.json") as file:
    service_account: dict[str, str] = json.load(file)
