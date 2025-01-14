#! /usr/bin/env python
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import SCHEDULE_UPDATE_TIME
from jobs import daily_check

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    chat_id = update.effective_chat.id  # type: ignore

    # Send welcome message
    await context.bot.send_message(
        chat_id=chat_id,  # type: ignore
        text=f'Bot will update the schedule every day at {SCHEDULE_UPDATE_TIME.strftime('%H:%M')} (GMT-3)',
    )

    job_queue = context.job_queue

    job_queue.run_daily(  # type: ignore
        daily_check,
        time=SCHEDULE_UPDATE_TIME,
        data=chat_id,  # type: ignore
    )


def main() -> None:
    token = os.getenv('TELEGRAM_TOKEN', '')
    if not token:
        exit('set the TELEGRAM_TOKEN variable.')

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start))

    app.run_polling()


if __name__ == '__main__':
    main()
