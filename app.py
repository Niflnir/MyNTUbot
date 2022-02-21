import logging
from pymongo import collection
import os
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from handlers.gpa import gpa_start, calc_gpa
from handlers.food_guide import (
    food_start,
    northHillFood,
    tamarindFood,
    hall11Food,
)
from handlers.useful_links import useful_links, course, faculty, year
from handlers.anonchat import anon_chat, anon_chat_start
from handlers.common_handlers import start, restart, cancel
from pymongo import MongoClient

# Connect to Mongodb cluster
cluster = MongoClient(os.environ.get("MONGODB"))

db = cluster["ntubot"]
collection = db["courseandyear"]
# collection.update_one(
#     {
#         "_id": 3,
#         "course": "computerscience",
#         "acadyear": "2019",
#         "url": "https://www.ntu.edu.sg/docs/librariesprovider118/ug/cs/ay2019/ay1920-scse-cs-programme-(24-may-2021).pdf?sfvrsn=74c72a12_2",
#     }
# )
# newvalues = {"$set": {"course": "computerscience"}}
# collection.update_one({"_id": 1}, newvalues)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def main():

    TOKEN = os.environ.get("TOKEN")
    PORT = int(os.environ.get("PORT", "80"))

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # To start the bot and open the start menu
    dispatcher.add_handler(CommandHandler("start", start))

    # Go back to start menu
    dispatcher.add_handler(
        CallbackQueryHandler(pattern="restart", callback=restart)
    )

    # For GPA helper
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(pattern="calc_gpa", callback=gpa_start)
            ],
            states={0: [MessageHandler(Filters.text, calc_gpa)]},
            fallbacks=[CommandHandler("cancel", cancel)],
        )
    )
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(pattern="food_guide", callback=food_start)
            ],
            states={
                0: [
                    CallbackQueryHandler(
                        pattern="northhill", callback=northHillFood
                    ),
                    CallbackQueryHandler(
                        pattern="hall10/11", callback=hall11Food
                    ),
                    CallbackQueryHandler(
                        pattern="tamarind", callback=tamarindFood
                    ),
                ]
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
    )

    # For anonymous chat
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(pattern="anon_chat", callback=anon_chat)
            ],
            states={0: [MessageHandler(Filters.text, anon_chat)]},
            fallbacks=[CommandHandler("cancel", cancel)],
        )
    )

    # For useful links like START, Degree Audit
    dispatcher.add_handler(
        CallbackQueryHandler(pattern="useful_links", callback=useful_links)
    )
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(pattern="curriculum", callback=faculty)
            ],
            states={
                0: [
                    CallbackQueryHandler(pattern="faculty_.*", callback=course)
                ],
                1: [CallbackQueryHandler(pattern="course_.*", callback=year)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
