#!/usr/bin/env python
import logging

from telegram.ext import ApplicationBuilder, JobQueue

from src.config import settings
from src.handlers import all_handlers
from src.jobs import schedule as schedule_jobs
from src.utils.global_utils import subtract_minutes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def setup_jobs(job_queue: JobQueue | None) -> None:
    """Sets up all of bot's jobs."""
    if job_queue is None:
        logging.error("job queue is None")
        return

    job_queue.run_daily(
        schedule_jobs.daily_schedule_update, time=settings.SCHEDULE_UPDATE_TIME
    )

    for time in settings.SCHEDULE_TIMES:
        job_queue.run_daily(
            schedule_jobs.notify_about_upcoming_lecture,
            time=subtract_minutes(time, settings.MINUTES_BEFORE_LECTURE),
            data={"original_time": time},
        )


def main() -> None:
    app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    setup_jobs(app.job_queue)

    app.add_handlers(all_handlers)

    app.run_polling()


if __name__ == "__main__":
    main()
