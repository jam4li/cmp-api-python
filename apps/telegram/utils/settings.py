from django.utils.translation import gettext as _
from apps.telegram.utils.base import *

from apps.telegram.models import TelegramLanguage


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [
            "Change language",
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(
        "Please choose",
        reply_markup=reply_markup,
    )

    return SETTINGS


async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("11")
    buttons = []
    button_text = update.message.text

    if _("Back") in button_text:
        await update.message.reply_text("Bang Bang")

    elif _("Change language") in button_text:
        await update.message.reply_text("1")
        language_list = TelegramLanguage.objects.all()
        await update.message.reply_text("2")

        for language in language_list:
            buttons.append(
                [
                    InlineKeyboardButton(
                        "1",
                        callback_data=language_code,
                    )
                ]
            )

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text("Please choose:", reply_markup=reply_markup)
