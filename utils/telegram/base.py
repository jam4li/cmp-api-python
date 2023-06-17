from django.utils.translation import gettext as _
import logging

from telegram import __version__ as TG_VER

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

HOME_MENU, EDUCATE, EDUCATE_CONTENT, START_OVER = range(4)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
