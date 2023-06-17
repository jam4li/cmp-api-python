from django.utils.translation import gettext as _
from utils.telegram.base import *

from apps.telegram.models import Educate, EducateContent


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
