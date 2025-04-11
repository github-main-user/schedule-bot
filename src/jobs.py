from datetime import datetime, timedelta

from telegram.ext import ContextTypes

from src.config import settings
from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository
from src.repositories.subscriber_repository import SubscriberRepository
from src.utils import messages


async def daily_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    session = await get_session()
    schedule_repo = ScheduleRepository(session)
    subscriber_repo = SubscriberRepository(session)

    tomorrow_date = datetime.now(settings.TIMEZONE).date() + timedelta(days=1)
    tomorrow_lectures = await schedule_repo.get_lectures_for_day(tomorrow_date)

    if tomorrow_lectures:
        message = messages.TOMORROW_N_LECTURES.format(n=len(tomorrow_lectures))
    else:
        message = messages.EMPTY_TOMORROW

    subscribers = await subscriber_repo.get_all()
    print(subscribers)

    for subscriber in subscribers:
        await context.bot.send_message(
            chat_id=subscriber.chat_id,
            text=message,
        )
