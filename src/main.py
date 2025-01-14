#! /usr/bin/env python
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import SCHEDULE_UPDATE_TIME, format_jobs
from jobs import daily_check

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    chat_id = update.effective_chat.id  # type: ignore
    job_queue = context.job_queue
    if job_queue.get_jobs_by_name('Daily Check'):  # type: ignore
        return

    await context.bot.send_message(
        chat_id=chat_id,  # type: ignore
        text=f'Bot will update the schedule every day at {SCHEDULE_UPDATE_TIME.strftime('%H:%M')} (GMT-3)',
    )

    job_queue.run_daily(  # type: ignore
        daily_check,
        time=SCHEDULE_UPDATE_TIME,
        data=chat_id,  # type: ignore
        name='Daily Check',
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id  # type: ignore
    jobs = context.job_queue.jobs()  # type: ignore

    await context.bot.send_message(
        chat_id=chat_id,  # type: ignore
        text=f'{format_jobs(jobs)}' if jobs else 'There are no active jobs',  # type: ignore
    )


def main() -> None:
    token = os.getenv('TELEGRAM_TOKEN', '')
    if not token:
        exit('set the TELEGRAM_TOKEN variable.')

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('status', status))

    app.run_polling()


if __name__ == '__main__':
    main()
