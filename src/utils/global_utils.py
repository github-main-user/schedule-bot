from datetime import date, datetime, time, timedelta

from src.config import settings


def get_local_now() -> datetime:
    """Returns a `datetime` (timezone aware) object with current time according to set in the settings timezone."""
    return datetime.now(settings.TIMEZONE)


def get_tomorrow() -> date:
    """Returns a `date` object containing tomorrow's date."""
    return date.today() + timedelta(days=1)


def subtract_minutes(original_time: time, minutes: int) -> time:
    """
    Subtracts given minutes from given `time`, since python doesn't provide builtin function to solve this problem.
    Returns another `time` object.
    """
    dummy_dt = datetime.combine(datetime.min, original_time)
    new_datetime = dummy_dt - timedelta(minutes=minutes)
    return new_datetime.time()
