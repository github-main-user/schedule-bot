import math
import parser
from datetime import datetime, timedelta

from telegram.ext import ContextTypes

from config import DAILY_TEMPLATE, MSK_TZ


async def send_lecture_info_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send inforemation about a specific lecture."""
    chat_id, date, lecture = context.job.data  # type: ignore

    await context.bot.send_message(
        chat_id=chat_id,  # type: ignore
        text=DAILY_TEMPLATE.format(
            minutes_left=math.ceil(
                (datetime.combine(date, lecture.time) - datetime.now()).total_seconds()
                / 60
            ),
            lecture_time=lecture.time.strftime('%H:%M'),
            lecture_name=lecture.discipline.name,
            cabinet=lecture.cabinet,
            teacher=lecture.teacher,
            is_practice='практика' if lecture.discipline.is_practice else 'лекция',
        ),
        parse_mode='Markdown',
    )


async def daily_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Perform the daily check to update the schedule."""
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
                    send_lecture_info_job,
                    when=datetime.combine(tomorrow_date, lecture.time, tzinfo=MSK_TZ)
                    - timedelta(minutes=15),
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
        await context.bot.send_message(
            chat_id=chat_id,  # type: ignore
            text="An error occurred while updating the schedule.",
        )
