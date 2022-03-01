import logging
import os
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)
import handlers


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def main():

    if os.environ.get("DEV"):
        TOKEN = os.environ.get("TEST_TOKEN")
    else:
        TOKEN = os.environ.get("TOKEN")
    PORT = int(os.environ.get("PORT", "80"))

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # To start the bot and open the start menu
    dispatcher.add_handler(CommandHandler("start", handlers.start))

    # Go back to start menu
    dispatcher.add_handler(
        CallbackQueryHandler(pattern="restart", callback=handlers.restart)
    )

    # For GPA helper
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    pattern="calc_gpa", callback=handlers.gpa_start
                )
            ],
            states={0: [MessageHandler(Filters.text, handlers.calc_gpa)]},
            fallbacks=[CommandHandler("cancel", handlers.cancel)],
        )
    )
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    pattern="food_guide", callback=handlers.food_start
                )
            ],
            states={
                0: [
                    CallbackQueryHandler(
                        pattern="northhill", callback=handlers.northHillFood
                    ),
                    CallbackQueryHandler(
                        pattern="hall10/11", callback=handlers.hall11Food
                    ),
                    CallbackQueryHandler(
                        pattern="tamarind",
                        callback=handlers.tamarindFood,
                    ),
                ]
            },
            fallbacks=[CommandHandler("cancel", handlers.cancel)],
        )
    )

    # For useful links like START, Degree Audit
    dispatcher.add_handler(
        CallbackQueryHandler(
            pattern="useful_links", callback=handlers.useful_links
        ),
    )
    dispatcher.add_handler(
        CallbackQueryHandler(
            pattern="useful_links_back", callback=handlers.useful_links
        ),
    )

    # Course curriculum
    dispatcher.add_handler(
        CallbackQueryHandler(pattern="curriculum", callback=handlers.faculty),
    )
    dispatcher.add_handler(
        CallbackQueryHandler(pattern="faculty_.*", callback=handlers.course),
    )
    dispatcher.add_handler(
        CallbackQueryHandler(pattern="course_.*", callback=handlers.year)
    )
    dispatcher.add_handler(
        CallbackQueryHandler(pattern="facultyback", callback=handlers.faculty),
    )

    # Quote of the day
    dispatcher.add_handler(
        CallbackQueryHandler(pattern="qotd", callback=handlers.qotd)
    )

    # WEBHOOK = os.environ.get("WEBHOOK")
    #
    # updater.start_webhook(
    #     listen="0.0.0.0",
    #     port=80,
    #     url_path=os.environ.get(TOKEN),
    # )
    # updater.bot.setWebhook(WEBHOOK + TOKEN)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
