from datetime import datetime

from telegram.ext import ContextTypes

from src.config import settings
from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository
from src.repositories.subscriber_repository import SubscriberRepository
from src.services.schedule import update_schedule
from src.utils import messages, schedule_utils


async def daily_schedule_update(context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_schedule()

    session = await get_session()
    schedule_repo = ScheduleRepository(session)
    subscriber_repo = SubscriberRepository(session)

    tomorrow_date = schedule_utils.get_tomorrow()
    tomorrow_lectures = await schedule_repo.get_lectures_for_day(tomorrow_date)

    subscribers = await subscriber_repo.get_all()

    for subscriber in subscribers:
        await context.bot.send_message(
            chat_id=subscriber.chat_id,
            text=(
                messages.TOMORROW_N_LECTURES.format(n=len(tomorrow_lectures))
                if tomorrow_lectures
                else messages.EMPTY_TOMORROW
            ),
        )
        if tomorrow_lectures:
            formatted_lectures = "\n".join([schedule_utils.format_lecture(lecture) for lecture in tomorrow_lectures])

            await context.bot.send_message(
                chat_id=subscriber.chat_id,
                text=(messages.DATE_TEMPLATE.format(date=tomorrow_date) + "\n" + formatted_lectures),
            )


async def notify_about_upcoming_lecture(context: ContextTypes.DEFAULT_TYPE) -> None:
    session = await get_session()

    schedule_repo = ScheduleRepository(session)
    subscriber_repo = SubscriberRepository(session)

    now = schedule_utils.get_local_now()
    next_lecture = await schedule_repo.get_next_lecture_after(now)

    if not next_lecture:
        return

    message = messages.LECTURE_VERBOSE_TEMPLATE.format(
        date=next_lecture.date_time.strftime("%d %b (%a)"),
        time=next_lecture.date_time.strftime("%H:%M"),
        name=next_lecture.discipline.name,
        cabinet=next_lecture.cabinet,
        is_practice="Практика" if next_lecture.is_practice else "Лекция",
        teacher=next_lecture.teacher.fullname,
        age=next_lecture.teacher.age,
    )

    subscribers = await subscriber_repo.get_all()
    for subscriber in subscribers:
        await context.bot.send_message(
            chat_id=subscriber.chat_id,
            text=message,
        )
