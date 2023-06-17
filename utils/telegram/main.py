from django.utils.translation import gettext as _
from django.conf import settings

from .base import *
from .start import start
from .home import home_menu
from .educate import educate_callback, educate_content_callback
from .cancel import cancel

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

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)


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
