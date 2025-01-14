from datetime import datetime, timedelta
from parser import ScheduleFormer

from telegram.ext import ContextTypes

from config import MSK_TZ, format_lectures, format_next_lecture


async def send_lecture_info_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send inforemation about a specific lecture."""
    chat_id, date, lecture = context.job.data  # type: ignore

    await context.bot.send_message(
        chat_id=chat_id,  # type: ignore
        text=format_next_lecture(lecture, date),
        parse_mode='Markdown',
    )


async def daily_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Perform the daily check to update the schedule."""
    chat_id = context.job.data  # type: ignore

    try:
        # Generate the schedule
        schedule = ScheduleFormer().form_schedule()
        tomorrow_date = (datetime.now(tz=MSK_TZ) + timedelta(days=1)).date()
        tomorrow_lectures = schedule.get(tomorrow_date, [])

        if tomorrow_lectures:
            await context.bot.send_message(
                chat_id=chat_id,  # type: ignore
                text=f"Tomorrow will be *{len(tomorrow_lectures)}* lecture(s):",
                parse_mode='Markdown',
            )

            # Schedule reminders for lectures
            for lecture in tomorrow_lectures:
                context.job_queue.run_once(  # type: ignore
                    send_lecture_info_job,
                    when=datetime.combine(tomorrow_date, lecture.time, tzinfo=MSK_TZ)
                    - timedelta(minutes=15),
                    data=(chat_id, tomorrow_date, lecture),
                    name=lecture.discipline.name,
                )

            await context.bot.send_message(
                chat_id=chat_id,  # type: ignore
                text=format_lectures(tomorrow_lectures, tomorrow_date),
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
