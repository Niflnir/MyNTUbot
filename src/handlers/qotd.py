import requests
from telegram import (
    Update,
)
from telegram.ext.callbackcontext import CallbackContext


def qotd(update: Update, context: CallbackContext):
    r = requests.get("https://api.yomomma.info/")
    joke = r.json()["joke"]
    update.callback_query.message.edit_text("QOTD:\n" + joke)
