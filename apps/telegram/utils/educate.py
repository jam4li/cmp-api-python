from django.utils.translation import gettext as _
from apps.telegram.utils.base import *

from apps.telegram.models import TelegramEducate, TelegramEducateContent


async def educate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = []
    educate_list = TelegramEducate.objects.all()

    async for educate in educate_list:
        buttons.append(
            [
                educate.name,
            ],
        )

    buttons.append(
        [
            "Back",
        ]
    )

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

    return EDUCATE


async def educate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("1")
    buttons = []
    button_text = update.message.text

    if _("Back") in button_text:
        await update.message.reply_text("Bang Bang")

    else:
        educate_obj = await TelegramEducate.objects.aget(name=button_text)
        educate_content_list = TelegramEducateContent.objects.filter(
            educate=educate_obj,
        )

        async for content in educate_content_list:
            buttons.append(
                [
                    content.title,
                ],
            )

        reply_markup = ReplyKeyboardMarkup(buttons)

        await update.message.reply_text("Please choose:", reply_markup=reply_markup)

        return EDUCATE_CONTENT


async def educate_content_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    educate_content = update.callback_query.data

    educate_obj = await TelegramEducateContent.objects.aget(id=educate_content)

    await update.callback_query.answer()
    await update.effective_message.edit_text(
        educate_obj.description,
    )

    return EDUCATE_CONTENT
