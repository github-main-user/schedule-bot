from datetime import date, datetime, time, timedelta

from src.config import settings


def get_local_now() -> datetime:
    """Returns a `datetime` (timezone aware) object with current time according to set in the settings timezone."""
    return datetime.now(settings.TIMEZONE)


def get_local_today() -> date:
    """
    Returns a `date` object which contains today's date.
    Uses the timezone from settings.
    """
    now = datetime.now(settings.TIMEZONE)
    return now.date()


def get_tomorrow() -> date:
    """
    Returns a `date` object which contains tomorrow's date.
    Uses the timezone from settings.
    """
    return get_local_today() + timedelta(days=1)


def subtract_minutes(original_time: time, minutes: int) -> time:
    """
    Subtracts given minutes from given `time`,
    since python doesn't provide builtin function to solve this problem.
    Returns timezone aware time.
    """
    dummy_dt = datetime.combine(datetime.max, original_time, tzinfo=settings.TIMEZONE)
    new_datetime = dummy_dt - timedelta(minutes=minutes)
    return new_datetime.timetz()
