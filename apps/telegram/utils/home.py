from django.utils.translation import gettext as _
from apps.telegram.utils.base import *

from apps.telegram.models import TelegramEducate, TelegramEducateContent
from utils.telegram.educate import educate
from utils.telegram.company import company
from utils.telegram.support import support
from utils.telegram.settings import settings


async def home_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    button_text = update.message.text

    if _("Educate") in button_text:
        await educate(update, context)

    elif _("Company") in button_text:
        await company(update, context)

    elif _("News") in button_text:
        await update.message.reply_text(
            "News News",
        )

    elif _("Support") in button_text:
        await support(update, context)

    elif _("Motivational") in button_text:
        await update.message.reply_text(
            "Motivational Motivational",
        )

    elif _("Settings") in button_text:
        await settings(update, context)
