from django.conf import settings
from django.utils.translation import gettext as _
from utils.telegram.base import *


async def company_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    company = update.callback_query.data

    if company == "branch":
        buttons = [
            [
                InlineKeyboardButton(
                    "Iran, Mashhad",
                    callback_data="1",
                ),
            ],
            [
                InlineKeyboardButton(
                    "Iran, Tehran",
                    callback_data="2",
                ),
            ],
            [
                InlineKeyboardButton(
                    "Iran, Isfahan",
                    callback_data="3",
                ),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.callback_query.answer()
        await update.effective_message.edit_text(
            "Please choose:",
            reply_markup=reply_markup,
        )

        return COMPANY_BRANCH


async def company_branch_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    chat_id = query.message.chat_id

    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
    )

    location = Location(
        latitude=40.7128,
        longitude=-74.0060,
    )

    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Address: Molla Sadra BLVD",
    )

    await bot.send_location(chat_id=chat_id, location=location)
