#! /usr/bin/env python
from datetime import datetime, time, timedelta
import logging
import os

import pytz
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import parser

load_dotenv()
MSK_TZ = pytz.timezone('Etc/GMT-3')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if effective_chat is None:
        logging.warning('Effective chat is None.')
        return

    # Send welcome message
    await context.bot.send_message(
        chat_id=effective_chat.id,
        text='Welcome! I will send you a message every day at 17:00 (UTC+3).',
    )

    # Schedule the job if not already scheduled
    chat_id = effective_chat.id
    job_queue = context.job_queue
    if job_queue is None:
        logging.warning('Job queue is None.')
        return
    current_jobs = job_queue.get_jobs_by_name(f'daily_message_{chat_id}')

    if not current_jobs is None:
        job_queue.run_daily(
            daily_check,
            time=time(hour=18, minute=0, tzinfo=MSK_TZ),
            data=chat_id,
            name=f'daily_message_{chat_id}',  # Unique name for the job
        )


async def daily_check(context: ContextTypes.DEFAULT_TYPE):
    # Ensure context.job exists
    if context.job is None:
        logging.warning("context.job is None.")
        return

    # Ensure context.job.data exists
    chat_id = context.job.data
    if not isinstance(chat_id, int | str):
        logging.warning(
            "context.job.data is not int or str. Cannot send scheduled message."
        )
        return

    sf = parser.ScheduleFormer()
    schedule = sf.form_schedule()
    tomorrow_date = (datetime.now(tz=MSK_TZ) + timedelta(days=1)).date()
    tomorrow_lectures = schedule.get(tomorrow_date, [])
    nearest_day = lectures[0] if len(lectures := sorted(schedule.keys())) > 0 else None

    # Send the daily message
    try:
        if len(tomorrow_lectures) > 0:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f'Tomorrow will be {len(tomorrow_lectures)} lectures.',
            )
        else:
            if nearest_day is not None:
                await context.bot.send_message(
                    chat_id=chat_id, text=f'The nearest lecture will be {nearest_day}.'
                )
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text=f'There is no lectures.'
                )
    except Exception as e:
        logging.error(f"Failed to send message to chat_id {chat_id}: {e}")


if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN', '')
    if not token:
        exit('set the TELEGRAM_TOKEN variable.')

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start))

    app.run_polling()
