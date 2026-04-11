import asyncio
import random

from src.core.firebase import initialize_firebase
from src.core.types import ServiceStatus

initialize_firebase()


def get_random_status() -> ServiceStatus:
    value = random.randint(1, 100)
    if value > 98:
        return "outage"
    elif value > 90:
        return "degraded"
    return "operational"


async def generate_reports() -> None:
    # TODO: add actual script
    pass


asyncio.run(generate_reports())
