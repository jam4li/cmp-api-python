from django.utils.translation import gettext as _
from utils.telegram.base import *

from apps.telegram.models import Educate, EducateContent


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
        deep_link = "https://t.me/defacer"
        buttons = [
            InlineKeyboardButton(
                "Chat with admin",
                url=deep_link,
            ),
        ],

        reply_markup = InlineKeyboardMarkup(buttons)

        user_id = update.message.from_user.id
        await update.message.reply_text("Choose the button to start", reply_markup=reply_markup)

        return HOME_MENU

    elif _("Motivational") in button_text:
        await update.message.reply_text(
            "Motivational Motivational",
        )

    elif _("Settings") in button_text:
        await update.message.reply_text(
            "Settings Settings",
        )
