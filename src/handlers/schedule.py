from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.config import settings
from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository
from src.utils import messages


async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None:
        return
    chat_id = update.effective_chat.id

    async with await get_session() as session:
        repo = ScheduleRepository(session)

        now = datetime.now(settings.TIMEZONE)
        next_lecture = await repo.get_next_lecture_after(now)
        if not next_lecture:
            return

        message = messages.LECTURE_TEMPLATE.format(
            date=next_lecture.date_time.strftime("%d %b (%a)"),
            time=next_lecture.date_time.strftime("%H:%M"),
            name=next_lecture.discipline.name,
            cabinet=next_lecture.cabinet,
            is_practice="Практика" if next_lecture.is_practice else "Лекция",
            teacher=next_lecture.teacher.fullname,
            age=next_lecture.teacher.age,
        )

    await context.bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="Markdown",
    )


schedule_handlers = [CommandHandler("next", next)]
