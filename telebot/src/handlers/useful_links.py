import os
import requests
from telegram import (
    Update,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
)
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton


def useful_links(update: Update, context: CallbackContext):
    update.callback_query.message.edit_text(
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
    r = requests.get(os.environ.get("API_URL") + "getfaculty").json()
    faculties = [
        InlineKeyboardButton(faculty, callback_data="faculty_" + faculty)
        for faculty in r
    ]

    update.callback_query.message.edit_text(
        "Please select the faculty",
        reply_markup=InlineKeyboardMarkup([faculties]),
    )
    return 0


# Select NTU course
def course(update: Update, context: CallbackContext):
    r = requests.get(
        os.environ.get("API_URL")
        + f"getcourse/{update.callback_query.data.split('_')[1]}"
    ).json()
    print(r)
    courses = [
        InlineKeyboardButton(
            coursename,
            callback_data="course_" + coursename,
        )
        for coursename in r
    ]

    update.callback_query.message.edit_text(
        "Please select the course",
        reply_markup=InlineKeyboardMarkup([courses]),
    )

    return 1


# Select NTU year
def year(update: Update, context: CallbackContext):
    r = requests.get(
        os.environ.get("API_URL")
        + f"geturls/{update.callback_query.data.split('_')[1]}"
    ).json()
    print("---------------------------------------------------------------")
    print(r)
    years = [InlineKeyboardButton(i["year"], url=i["url"]) for i in r]
    update.callback_query.message.edit_text(
        "Please select the year",
        reply_markup=InlineKeyboardMarkup([years]),
    )
