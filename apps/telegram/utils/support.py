from django.utils.translation import gettext as _
from apps.telegram.utils.base import *

from apps.telegram.models import TelegramConfig


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    telegram_config = await TelegramConfig.objects.get_or_create_singleton()

    deep_link = "https://t.me/" + telegram_config.support_username
    buttons = [
        [
            "FAQ (Frequently Asked Questions)",
        ],
        [
            "Chat with admin",
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    # user_id = update.message.from_user.id
    await update.message.reply_text("Choose the button", reply_markup=reply_markup)

    return HOME_MENU
