from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.config import settings
from src.utils import messages


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_chat:
        return

    message = messages.HELP.format(
        update_time=settings.SCHEDULE_UPDATE_TIME,
        minutes_before=settings.MINUTES_BEFORE_LECTURE,
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
    )


special_handlers = [CommandHandler("help", help)]
