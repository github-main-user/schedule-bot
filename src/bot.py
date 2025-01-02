#! /usr/bin/env python

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logging.warning('Effective chat is None.')
        return

    await context.bot.send_message(
        chat_id=effective_chat.id,
        text='test',
    )


if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN', '')
    if not token:
        exit('set the TELEGRAM_TOKEN variable.')

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start))

    app.run_polling()
