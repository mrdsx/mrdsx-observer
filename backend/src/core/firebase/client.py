from dotenv import load_dotenv
from firebase_admin import initialize_app  # pyright: ignore[reportUnknownVariableType]
from firebase_admin.credentials import Certificate

from .config import service_account

load_dotenv()


def initialize_firebase() -> None:
    initialize_app(credential=Certificate(service_account))
