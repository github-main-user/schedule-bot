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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    chat_id = update.effective_chat.id  # type: ignore

    # Send welcome message
    await context.bot.send_message(
        chat_id=chat_id,  # type: ignore
        text='Bot will update the schedule every day at 22:00 (GMT-3)',
    )

    job_queue = context.job_queue

    job_queue.run_daily(  # type: ignore
        daily_check,
        time=time(hour=22, minute=0, tzinfo=MSK_TZ),
        data=chat_id,  # type: ignore
    )


async def send_lecture_info(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send inforemation about a specific lecture."""
    chat_id, date, lecture = context.job.data  # type: ignore

    await context.bot.send_message(
        chat_id=chat_id,  # type: ignore
        text=f'{int((datetime.combine(date, lecture.time) - datetime.now()).total_seconds() / 60)} minutes left before the next lecture:'
        f'\n*{lecture.time.strftime('%H:%M')}*: {lecture.discipline.name} ({lecture.cabinet})'
        f'\n{lecture.teacher} ({'практика' if lecture.discipline.is_practice else 'лекция'})',
        parse_mode='Markdown',
    )


async def daily_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Perform the daily check to update the schedule."""
    # Ensure context.job.data exists
    chat_id = context.job.data  # type: ignore

    try:
        # Generate the schedule
        schedule = parser.ScheduleFormer().form_schedule()
        tomorrow_date = (datetime.now(tz=MSK_TZ) + timedelta(days=1)).date()
        tomorrow_lectures = schedule.get(tomorrow_date, [])

        if tomorrow_lectures:
            await context.bot.send_message(
                chat_id=chat_id,  # type: ignore
                text=f"Tomorrow will be *{len(tomorrow_lectures)}* lecture(s):",
                parse_mode='Markdown',
            )

            formatted_lectures = [tomorrow_date.strftime('*%d %b (%a)*')]
            # Schedule reminders for lectures
            for lecture in tomorrow_lectures:
                formatted_lectures.append(
                    f'*{lecture.time.strftime('%H:%M')}*: {lecture.discipline.name} ({lecture.cabinet})'
                )
                context.job_queue.run_once(  # type: ignore
                    send_lecture_info,
                    when=datetime.combine(tomorrow_date, lecture.time, tzinfo=MSK_TZ),
                    data=(chat_id, tomorrow_date, lecture),
                )

            await context.bot.send_message(
                chat_id=chat_id,  # type: ignore
                text=f"{'\n'.join(formatted_lectures)}",
                parse_mode='Markdown',
            )
        else:
            # Notify about the next lecture day
            nearest_day = min(schedule.keys()) if schedule else None
            if nearest_day:
                await context.bot.send_message(
                    chat_id=chat_id,  # type: ignore
                    text=f"The nearest lecture will be on {nearest_day.strftime('%d %b, %a')} ({(nearest_day - datetime.now().date()).days} day(s)).",
                )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,  # type: ignore
                    text="There are no upcoming lectures.",
                )
    except Exception as e:
        logging.error(f"Error in daily_check: {e}")
        await context.bot.send_message(
            chat_id=chat_id,  # type: ignore
            text="An error occurred while updating the schedule.",
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
