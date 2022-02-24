from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton


def food_start(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text(
        "Where would you like to eat?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        "North Hill", callback_data="northhill"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Hall 10/11", callback_data="hall10/11"
                    )
                ],
                [InlineKeyboardButton("Tamarind", callback_data="tamarind")],
                [InlineKeyboardButton("Back", callback_data="restart")],
            ]
        ),
    )
    return 0


def northHillFood(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text(
        """
Stalls             Recommendations

Indian             Prata with Egg set ($3)
Chicken rice       Chicken rice ($3.50)
Mixed rice         Rice with 2 Veggies ($4.50)
Taiwan             XL pork chop rice ($5)
Western            Fish & Chips ($4.80)
Thai/Noodles       Minced Meat Noodles ($4)
Chinese            Chicken Fried Rice ($3.50)
Mala 

        """
    )
    return ConversationHandler.END


def tamarindFood(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text(
        """
Stalls          Recommendations

Indian          Ayam Panggang ($5)
Chicken rice    Chicken rice ($3.50) 
Korean          Beef Bulgogi ($4) 
Western         Pasta with cream sauce ($5)
Mala            Fish & Chips ($4.80)
Thai/Noodles    Minced Meat Noodles ($5)
Chinese         Chicken Fried Rice ($3.50)


        """
    )
    return ConversationHandler.END


def hall11Food(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text(
        """
Stalls          Recommendations

Indian          Prata with Egg set ($3)
Chicken rice    Chicken rice ($3.50) 
Mixed rice      Rice with 2 Veggies ($4.50) 
Taiwan          XL pork chop rice ($5)
Western         Fish & Chips ($4.80)
Thai/Noodles    
Chinese         Chicken Fried Rice ($3.50)
Mala            

        """
    )
    return ConversationHandler.END
