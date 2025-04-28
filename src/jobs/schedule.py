import logging
from datetime import datetime, time

from telegram.ext import ContextTypes

from src.config import settings
from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository
from src.repositories.subscriber_repository import SubscriberRepository
from src.services.schedule import update_schedule
from src.utils import global_utils, messages, schedule_utils

logger = logging.getLogger(__name__)


async def daily_schedule_update(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Updates the local schedule.
    Notifies all subscribed users about tomorrow lectures.
    """

    logger.info("Starting daily update job")

    await update_schedule()

    async with await get_session() as session:
        schedule_repo = ScheduleRepository(session)
        subscriber_repo = SubscriberRepository(session)

        tomorrow_date = global_utils.get_local_tomorrow()
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
            await context.bot.send_message(
                chat_id=subscriber.chat_id,
                text=schedule_utils.format_lectures_by_their_dates(tomorrow_lectures),
                parse_mode="Markdown",
            )

        logger.info(
            "Subscribed user %s was notified about tomorrow lectures",
            subscriber.chat_id,
        )


async def notify_about_upcoming_lecture(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fetches a lecture for a specific time.
    If there is notifies all subscribed users about upcoming lecture.
    """
    logger.info("Starting per lecture job")

    job = context.job
    if not job:
        logger.warning("Job is None, leaving")
        return

    lecture_time: time = job.data.get("original_time")  # type: ignore
    exact_lecture_datetime = datetime.combine(
        date=global_utils.get_local_today(),
        time=lecture_time,
        tzinfo=settings.TIMEZONE,
    )

    async with await get_session() as session:
        schedule_repo = ScheduleRepository(session)
        subscriber_repo = SubscriberRepository(session)

        next_lecture = await schedule_repo.get_lecture_by_datetime(
            exact_lecture_datetime
        )

        if not next_lecture:
            logger.info("There is no lecture at %s, leaving", exact_lecture_datetime)
            return

        subscribers = await subscriber_repo.get_all()

    for subscriber in subscribers:
        await context.bot.send_message(
            chat_id=subscriber.chat_id,
            text=schedule_utils.format_lecture_verbose(next_lecture),
        )
        logger.info(
            "Subscribed user %s was notified about upcoming lecture", subscriber.chat_id
        )
