from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.utils import messages


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_chat:
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.HELP,
    )


special_handlers = [CommandHandler("help", help)]
