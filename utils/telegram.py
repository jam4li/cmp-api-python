from django.conf import settings
from django.utils.translation import gettext as _
from asgiref.sync import sync_to_async

import logging

from telegram import __version__ as TG_VER

from apps.telegram.models import Educate, EducateContent

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
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

HOME_MENU, EDUCATE, EDUCATE_CONTENT = range(3)

START_OVER = range(3, 4)

# Define a few command handlers. These usually take the two arguments update and
# context.


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


async def home_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    button_text = update.message.text

    await update.message.reply_text(
        button_text,
    )

    if _("Educate") in button_text:
        buttons = []
        educate_list = Educate.objects.all()

        async for educate in educate_list:
            buttons.append(
                [
                    InlineKeyboardButton(
                        educate.name,
                        callback_data=str(educate.id),
                    ),
                ],
            )

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text("Please choose:", reply_markup=reply_markup)

        return EDUCATE

    elif _("Company") in button_text:
        await update.message.reply_text(
            "Company Company",
        )

    elif _("Violations") in button_text:
        await update.message.reply_text(
            "Violations Violations",
        )

    elif _("News") in button_text:
        await update.message.reply_text(
            "News News",
        )

    elif _("Support") in button_text:
        await update.message.reply_text(
            "Support Support",
        )

    elif _("Motivational") in button_text:
        await update.message.reply_text(
            "Motivational Motivational",
        )

    elif _("Settings") in button_text:
        await update.message.reply_text(
            "Settings Settings",
        )

    # return HOME_MENU


async def educate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = []
    educate = update.callback_query.data

    educate_obj = await Educate.objects.aget(id=educate)
    educate_content_list = EducateContent.objects.filter(
        educate=educate_obj,
    )

    async for content in educate_content_list:
        buttons.append(
            [
                InlineKeyboardButton(
                    content.title,
                    callback_data=str(content.id),
                ),
            ],
        )

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Please choose:",
        reply_markup=reply_markup,
    )

    return EDUCATE_CONTENT


async def educate_content_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    educate_content = update.callback_query.data

    educate_obj = await EducateContent.objects.aget(id=educate_content)

    await update.callback_query.answer()
    await update.effective_message.edit_text(
        educate_obj.description,
    )

    return EDUCATE_CONTENT


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
    logger.info(
        "Start the bot",
    )
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler(
                "start",
                start,
            ),
        ],
        states={
            HOME_MENU: [
                MessageHandler(
                    filters.TEXT,
                    home_menu,
                ),
            ],
            EDUCATE: [
                CallbackQueryHandler(
                    educate_callback,
                ),
            ],
            EDUCATE_CONTENT: [
                CallbackQueryHandler(
                    educate_content_callback,
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

    application.add_handler(conversation_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()


def run_bot():
    main()
