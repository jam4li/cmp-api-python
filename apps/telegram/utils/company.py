from django.conf import settings
from django.utils.translation import gettext as _
from apps.telegram.utils.base import *


async def company(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [
            "\U0001f3e2" + " " + "Offices",
            "\U0001f3a4" + " " + "Seminars",
        ],
        [
            "Violation",
            "Business Cards",
        ],
        [
            "About Us",
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(
        "Please choose",
        reply_markup=reply_markup,
    )

    return COMPANY


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

        return COMPANY_OFFICE

    elif company == "seminar":
        buttons = [
            [
                InlineKeyboardButton(
                    "Mashhad 2023",
                    callback_data="1",
                ),
            ],
            [
                InlineKeyboardButton(
                    "Tehran 2022",
                    callback_data="2",
                ),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.callback_query.answer()
        await update.effective_message.edit_text(
            "Please choose:",
            reply_markup=reply_markup,
        )

        return COMPANY_SEMINAR

    elif company == "business_card":
        await update.callback_query.answer()
        await update.effective_message.edit_text(
            "There are some business cards:",
        )

        return COMPANY


async def company_office_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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


async def company_seminar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    chat_id = query.message.chat_id

    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
    )

    banner = await Banner.objects.aget(id=1)

    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "This is a test",
    )

    await bot.send_photo(chat_id=chat_id, photo="https://upload.wikimedia.org/wikipedia/commons/c/c9/Moon.jpg")
