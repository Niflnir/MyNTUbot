from pymongo import MongoClient
import os
from telegram import (
    Update,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
)
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
import sys

sys.path.append("../")
import mongosetup


def useful_links(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text(
        "Hi! What would you like to do?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        "STARS",
                        url="https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Degree Audit",
                        url="https://venus.wis.ntu.edu.sg/PortalServices/ServiceListModule/LaunchService.aspx?type=1&launchSvc=https%3A%2F%2Fwish%2Ewis%2Entu%2Eedu%2Esg%2Fpls%2Fwebexe%2Fldap%5Flogin%2Elogin%3Fw%5Furl%3Dhttps%3A%2F%2Fwish%2Ewis%2Entu%2Eedu%2Esg%2Fpls%2Fwebexe%2Fdars%5Fresult%5Fro%2Emain%5Fdisplay",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Course Curriculum Structure",
                        callback_data="curriculum",
                    )
                ],
                [InlineKeyboardButton("Back", callback_data="restart")],
            ]
        ),
    )


def faculty(update: Update, context: CallbackContext):
    collection = mongosetup.mongo("courseandyear")
    print(collection.find())
    faculties = [
        InlineKeyboardButton(
            i["faculty"], callback_data="faculty_" + i["faculty"]
        )
        for i in collection.find()
    ]

    update.callback_query.message.reply_text(
        "Please select the faculty",
        reply_markup=InlineKeyboardMarkup([faculties]),
    )
    return 0


# Select NTU course
def course(update: Update, context: CallbackContext):
    collection = mongosetup.mongo("courseandyear")
    courses = [
        InlineKeyboardButton(
            i["coursename"],
            callback_data="course_" + i["coursename"],
        )
        for i in collection.find_one(
            {"faculty": update.callback_query.data.split("_")[1]}
        )["courses"]
    ]

    update.callback_query.message.reply_text(
        "Please select the year",
        reply_markup=InlineKeyboardMarkup([courses]),
    )

    return 1


# Select NTU year
def year(update: Update, context: CallbackContext):
    collection = mongosetup.mongo("courseandyear")
    course_name = update.callback_query.data.split("_")[1]
    years = []
    for i in collection.find_one({"courses.coursename": course_name})[
        "courses"
    ]:
        if i["coursename"] == course_name:
            for j in i["urls"]:
                years.append(InlineKeyboardButton(j["year"], url=j["url"]))

    update.callback_query.message.reply_text(
        "Please select the year",
        reply_markup=InlineKeyboardMarkup([years]),
    )
