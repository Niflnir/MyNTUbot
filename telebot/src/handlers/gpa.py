from telegram import (
    Update,
)
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)


def gpa_start(update: Update, context: CallbackContext):
    update.callback_query.message.edit_text(
        "Please enter the number of AUs and the grade for the mods."
    )
    update.callback_query.message.reply_text(
        """
Example:
3 A
3 B+
4 B+
3 B+
3 A-
Spacing is important!!!
"""
    )
    return 0


def gradeToNum(grade) -> int:
    gradeToNumDict = {
        "a+": 5.0,
        "a": 5.0,
        "a-": 4.5,
        "b+": 4.0,
        "b": 3.5,
        "b-": 3.0,
        "c+": 2.5,
        "c": 2.0,
        "c-": 1.5,
        "d+": 1.0,
        "d": 0.5,
        "d-": 0,
        "e": 0,
        "f": 0,
        "A+": 5.0,
        "A": 5.0,
        "A-": 4.5,
        "B+": 4.0,
        "B": 3.5,
        "B-": 3.0,
        "C+": 2.5,
        "C": 2.0,
        "C-": 1.5,
        "D+": 1.0,
        "D": 0.5,
        "D-": 0,
        "E": 0,
        "F": 0,
    }

    return gradeToNumDict[grade]


def calc_gpa(update: Update, context: CallbackContext):
    msg = update.message.text.split("\n")
    total_aus = 0
    running_sum = 0
    try:
        for line in msg:
            aus, grade = line.split(" ")
            numGrade = gradeToNum(grade)
            total_aus += int(aus)
            running_sum += float(numGrade) * int(aus)

        update.message.reply_text(f"Your GPA is {(running_sum/total_aus):.2f}")

    except Exception as e:
        print(str(e))
        update.message.reply_text("TRY AGAIN PLEASE")
        return 0

    return ConversationHandler.END
