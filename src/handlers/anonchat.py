import json
import logging
import requests
import os
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    callbackcontext,
)
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton


def anon_chat_start(update: Update, context: CallbackContext):
    pass


def anon_chat(update: Update, context: CallbackContext):
    pass
