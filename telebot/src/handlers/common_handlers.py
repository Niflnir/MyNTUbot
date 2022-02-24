import logging
from telegram import (
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
import requests


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    userinfo = update.message.from_user
    chat_id = update.message.chat_id

    try:
        requests.put(
            "localhost:3000", data={"_id": chat_id, "username": userinfo}
        )
    except Exception as e:
        print(e)

    update.message.reply_text(
        "Hi! What would you like to do?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        "Calculate GPA",
                        callback_data="calc_gpa",  # name of the callback data to identify in CallbackQueryHandler
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Food Guide", callback_data="food_guide"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Useful Links", callback_data="useful_links"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Quote of the Day", callback_data="qotd"
                    )
                ],
            ]
        ),
    )


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.username)
    update.message.reply_text(
        "Bye! Have a nice day!",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def restart(update: Update, context: CallbackContext):
    update.callback_query.message.edit_text(
        "Hi! What would you like to do?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        "Calculate GPA",
                        callback_data="calc_gpa",  # name of the callback data to identify in CallbackQueryHandler
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Food Guide", callback_data="food_guide"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Useful Links", callback_data="useful_links"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Quote of the Day", callback_data="qotd"
                    )
                ],
            ]
        ),
    )
