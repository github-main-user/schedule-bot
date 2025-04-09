import requests

from src.config import settings


def request_raw_schedule() -> list:
    r = requests.get(url=settings.SCHEDULE_URL, timeout=5)
    r.raise_for_status()

    return r.json().get("scheduleChanges", [])
