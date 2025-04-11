#! /usr/bin/env python
import logging

from telegram.ext import ApplicationBuilder

from src.config import settings
from src.handlers.subscribers import command_handlers
from src.jobs import daily_check

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def main() -> None:
    app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    app.add_handlers(command_handlers)

    job_queue = app.job_queue
    if not job_queue:
        logging.error("job queue is None")
        return

    job_queue.run_once(daily_check, 0)

    app.run_polling()


if __name__ == "__main__":
    main()
