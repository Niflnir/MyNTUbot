import os
from pymongo import MongoClient
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


def start(update: Update, context: CallbackContext) -> int:
    cluster = MongoClient(os.environ.get("MONGODB"))
    db = cluster["ntubot"]
    collection = db["studentinfo"]

    userinfo = update.message.from_user
    chat_id = update.message.chat_id

    if collection.find_one({"_id": chat_id}) is None:
        userinfo = {"_id": chat_id, "username": userinfo["username"]}
        collection.insert_one(userinfo)

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
                [InlineKeyboardButton("Anon Chat", callback_data="anon_chat")],
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
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def restart(update: Update, _context: CallbackContext):
    update.callback_query.message.reply_text(
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
                [InlineKeyboardButton("Anon Chat", callback_data="anon_chat")],
                [
                    InlineKeyboardButton(
                        "Useful Links", callback_data="useful_links"
                    )
                ],
            ]
        ),
    )
