#! /usr/bin/env python
import logging

from telegram.ext import ApplicationBuilder, JobQueue

from src import jobs
from src.config import settings
from src.handlers.schedule import schedule_handlers
from src.handlers.special import special_handlers
from src.handlers.subscribers import command_handlers
from src.utils.schedule_utils import subtract_minutes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def setup_jobs(job_queue: JobQueue | None) -> None:
    if job_queue is None:
        logging.error("job queue is None")
        return

    job_queue.run_daily(jobs.daily_check_job, time=settings.SCHEDULE_UPDATE_TIME)

    for time in settings.SCHEDULE_TIMES:
        job_queue.run_daily(
            jobs.notify_about_upcoming_lecture,
            time=subtract_minutes(time, settings.MINUTES_BEFORE_LECTURE),
        )


def main() -> None:
    app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    setup_jobs(app.job_queue)

    app.add_handlers(command_handlers)
    app.add_handlers(special_handlers)
    app.add_handlers(schedule_handlers)

    app.run_polling()


if __name__ == "__main__":
    main()
