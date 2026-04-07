from dotenv import load_dotenv
from firebase_admin import initialize_app  # pyright: ignore[reportUnknownVariableType]
from firebase_admin.credentials import Certificate

from .config import service_account

# ! NEVER DELETE THIS LINE
# otherwise app can't inject firebase emulators hosts
# and firebase will connect to production databaseE
load_dotenv()


def initialize_firebase() -> None:
    initialize_app(credential=Certificate(service_account))
