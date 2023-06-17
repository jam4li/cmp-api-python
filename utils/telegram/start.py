from django.utils.translation import gettext as _
from utils.telegram.base import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler."""

    text = str(
        "\U0001F44B" + " Welcome to our Financial Service Bot! " + "\U0001F44B" + "\n"
        "We're delighted to have you here." + "\n"
        "Our mission is to assist you in making smarter financial decisions with confidence." + "\n" + "\n"
        "Here, you can:" + "\n"
        "\u0031\u20E3" + " Get detailed information about our financial products and services." + "\n"
        "\u0032\u20E3" + " Request assistance from our dedicated customer support team." + "\n"
        "\u0033\u20E3" + " Access financial tips and advice tailored to your needs." + "\n"
        "To get started, please choose your preferred language and follow the prompts." + "\n"
        "If you need any help, simply type '/help' at any time." + "\n"
        "You can also type '/cancel'.",
    )

    buttons = [
        [
            "\U0001F4D6" + " " + _("Educate"),
            "\U0001F310" + " " + _("Company"),
        ],
        # [
        # "\U0001F3A4" + " " + _("Seminars"),
        # "\U00002139" + " " + _("About Us"),
        # "\U0001F3E2" + " " + _("Offices"),
        # ],
        [
            "\U0001F6AB" + " " + _("Violations"),
            "\U0001F4E3" + " " + _("News"),
        ],
        [
            "\U0001F4AC" + " " + _("Support"),
            "\U00002728" + " " + _("Motivational"),
        ],
        [
            "\u2699\ufe0f" + " " + _("Settings"),
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

    context.user_data[START_OVER] = False
    return HOME_MENU
