#! /usr/bin/env python
import logging

from telegram.ext import ApplicationBuilder, JobQueue

from src.config import settings
from src.handlers.subscribers import command_handlers
from src.jobs import daily_check_job

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def setup_jobs(job_queue: JobQueue | None):
    if job_queue is None:
        logging.error("job queue is None")
        return

    job_queue.run_daily(daily_check_job, time=settings.SCHEDULE_UPDATE_TIME)


def main() -> None:
    app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    app.add_handlers(command_handlers)
    setup_jobs(app.job_queue)

    app.run_polling()


if __name__ == "__main__":
    main()
