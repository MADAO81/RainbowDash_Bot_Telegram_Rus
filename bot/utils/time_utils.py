"""
Утилиты для работы со временем.
Проверка рабочего времени бота.

Автор: MADAO81
Версия: 1.0
"""

from datetime import datetime
from bot.config import Config


def is_working_hours() -> bool:
    """Проверяет, рабочее ли сейчас время."""
    current_hour = datetime.now().hour
    return Config.WORK_START_HOUR <= current_hour < Config.WORK_END_HOUR


def get_working_status_message() -> str:
    """Возвращает сообщение о нерабочем времени."""
    return f"⏰ Бот работает с {Config.WORK_START_HOUR}:00 до {Config.WORK_END_HOUR}:00\nПриходи позже! 🌈"
