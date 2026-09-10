"""
Главный модуль бота Рэйнбоу Дэш.

Автор: MADAO81
Версия: 1.1 — выборочное логирование (убираем DEBUG-спам от httpcore/httpx/telegram)
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.config import Config
from bot.handlers.commands import start, help_command, weather_command
from bot.handlers.extra import (
    sport_command,
    rock_command,
    harley_command,
    challenge_command,
    motivate_command,
    truth_command
)
from bot.handlers.messages import handle_message
from bot.handlers.photos import handle_photo
from bot.handlers.voice import handle_voice
from bot.handlers.admin import admin_panel
from bot.core.scheduler import start_scheduler, subscribe_command, unsubscribe_command
from bot.core.reminder_scheduler import start_reminder_scheduler
from bot.core.constants import VERSION

# Базовое логирование для нашего бота — INFO
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Отключаем шумные библиотеки — они не должны спамить в логи
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Включаем DEBUG только для нашего бота (если нужно)
if Config.DEBUG_MODE:
    # Логируем всё, что наш бот пишет
    logging.getLogger("bot").setLevel(logging.DEBUG)
    logger.info("🐛 DEBUG_MODE включён (только для модулей 'bot')")


def main():
    logger.info(f"🌈 Запуск бота Рэйнбоу Дэш (v{VERSION})...")
    logger.info(f"👤 Автор: MADAO81")

    if not Config.TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN не найден в .env файле!")
        return

    if not Config.PROXY_API_KEY:
        logger.error("❌ PROXY_API_KEY не найден в .env файле!")
        return

    app = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    # Подписки
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))

    # Основные команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather_command))

    # Команды Рэйнбоу
    app.add_handler(CommandHandler("sport", sport_command))
    app.add_handler(CommandHandler("rock", rock_command))
    app.add_handler(CommandHandler("harley", harley_command))
    app.add_handler(CommandHandler("challenge", challenge_command))
    app.add_handler(CommandHandler("motivate", motivate_command))
    app.add_handler(CommandHandler("truth", truth_command))

    # Админ
    app.add_handler(CommandHandler("admin", admin_panel))

    # Обработчики сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.AUDIO, handle_voice))

    # Планировщики
    start_scheduler(app)
    start_reminder_scheduler(app)

    logger.info("✅ Бот Рэйнбоу Дэш успешно запущен и готов к работе!")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
