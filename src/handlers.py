from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.config import settings
from src.utils import messages


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None:
        return

    chat_id = update.effective_chat.id

    subscribe_msg = messages.SUBSCRIBE.format(time=settings.SCHEDULE_UPDATE_TIME.strftime("%H:%M"))
    await context.bot.send_message(
        chat_id=chat_id,
        text=subscribe_msg,
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None:
        return

    chat_id = update.effective_chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text=messages.UNSUBSCRIBE,
    )


command_handlers = [
    CommandHandler("start", start),
    CommandHandler("stop", stop),
]
