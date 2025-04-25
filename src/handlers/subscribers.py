import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.config import settings
from src.db import get_session
from src.repositories.subscriber_repository import SubscriberRepository
from src.utils import messages
from src.utils.bot_utils import with_chat_id

logger = logging.getLogger(__name__)


@with_chat_id
async def start(chat_id: int, _update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /start command.
    Subscribes user if it is not already subscribed.
    """

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


@with_chat_id
async def stop(chat_id: int, _update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /stop command.
    Unsubscribes user if it is subscribed.
    """

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
