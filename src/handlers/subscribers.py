import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.config import settings
from src.db import get_session
from src.repositories.subscriber_repository import SubscriberRepository
from src.utils import messages

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /start command.
    Subscribes user if it is not already subscribed.
    """
    if update.effective_chat is None:
        logger.warning("Effective chat is None")
        return
    chat_id = update.effective_chat.id

    async with await get_session() as session:
        repo = SubscriberRepository(session)

        if await repo.exists(chat_id):
            logger.info("User %s is already subscribed", chat_id)
            message = messages.ALREADY_SUBSCRIBED
        else:
            await repo.create(chat_id)
            logger.info("User %s subscribed successfully", chat_id)
            message = messages.SUBSCRIBED.format(update_time=settings.SCHEDULE_UPDATE_TIME)

    await context.bot.send_message(chat_id=chat_id, text=message)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /stop command.
    Unsubscribes user it it is subscribed.
    """
    if update.effective_chat is None:
        logger.warning("Effective chat is None")
        return
    chat_id = update.effective_chat.id

    async with await get_session() as session:
        repo = SubscriberRepository(session)

        if await repo.exists(chat_id):
            await repo.delete(chat_id)
            logger.info("User %s unsubscribed successfully", chat_id)
            message = messages.UNSUBSCRIBED
        else:
            logger.info("User %s is not subscribed", chat_id)
            message = messages.NOT_SUBSCRIBED

    await context.bot.send_message(chat_id=chat_id, text=message)


command_handlers = [
    CommandHandler("start", start),
    CommandHandler("stop", stop),
]
