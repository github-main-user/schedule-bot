from datetime import date, datetime, time, timedelta

from src.config import settings


def get_local_now() -> datetime:
    return datetime.now(settings.TIMEZONE)


def get_tomorrow() -> date:
    return date.today() + timedelta(days=1)


def subtract_minutes(original_time: time, minutes: int) -> time:
    dummy_dt = datetime.combine(datetime.min, original_time)
    new_datetime = dummy_dt - timedelta(minutes=minutes)
    return new_datetime.time()
