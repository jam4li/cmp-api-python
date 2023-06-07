from django.conf import settings
from django.utils.translation import gettext as _

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

# Define a few command handlers. These usually take the two arguments update and
# context.


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user to choose the language."""

    reply_keyboard = [
        [
            "\U0001F1EC\U0001F1E7" + " " + _("English"),
            "\U0001F1EE\U0001F1F7" + " " + _("Persian"),
        ],
        [
            "\U0001F1F8\U0001F1E6" + " " + _("Arabic"),
            "\U0001F1F9\U0001F1F7" + " " + _("Turkish"),
        ],
    ]

    await update.message.reply_text(
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
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Choose your language",
        ),
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info(
        "Gender of %s: %s",
        user.first_name,
        update.message.text,
    )

    await update.message.reply_text(
        "To proceed, please choose the action you're interested in." + "\n"
        "If you need any help, simply type '/help' at any time.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder="Select",
        ),
    )

    return PHOTO


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info(
        "User %s did not send a location.",
        user.first_name,
    )
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info(
        "Bio of %s: %s", user.first_name,
        update.message.text,
    )
    await update.message.reply_text(
        "Thank you! I hope we can talk again some day.",
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info(
        "User %s canceled the conversation.",
        user.first_name,
    )
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler(
                "start",
                start,
            ),
        ],
        states={
            GENDER: [
                MessageHandler(
                    filters.Regex("^(Boy|Girl|Other)$"),
                    gender,
                ),
            ],
            LOCATION: [
                MessageHandler(
                    filters.LOCATION,
                    location,
                ),
                CommandHandler(
                    "skip",
                    skip_location,
                ),
            ],
        },
        fallbacks=[
            CommandHandler(
                "cancel",
                cancel,
            ),
        ],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()


def run_bot():
    main()
