#! /usr/bin/env python
import logging

from telegram.ext import ApplicationBuilder

from src.config import settings
from src.handlers import command_handlers

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def main() -> None:
    app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    app.add_handlers(command_handlers)
    app.run_polling()


if __name__ == "__main__":
    main()
