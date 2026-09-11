"""
Конфигурация бота Рэйнбоу Дэш.
Загрузка переменных окружения из .env файла.

Автор: MADAO81
Версия: 1.1 — добавлены ID создателя для пасхалки
"""

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    """Класс конфигурации бота."""

    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    # ProxyAPI (DeepSeek)
    PROXY_API_KEY = os.getenv("PROXY_API_KEY")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek/deepseek-v4-flash")
    DEEPSEEK_MAX_TOKENS = int(os.getenv("DEEPSEEK_MAX_TOKENS", 2000))
    DEEPSEEK_TEMPERATURE = float(os.getenv("DEEPSEEK_TEMPERATURE", 0.9))

    # OpenAI (для голоса)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 1000))
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.85))

    # Координаты Ворсино
    DEFAULT_LAT = float(os.getenv("DEFAULT_LAT", 55.0965))
    DEFAULT_LON = float(os.getenv("DEFAULT_LON", 36.6355))

    # Рабочее время
    WORK_START_HOUR = int(os.getenv("WORK_START_HOUR", 9))
    WORK_END_HOUR = int(os.getenv("WORK_END_HOUR", 22))
    CONTEXT_EXPIRE_DAYS = int(os.getenv("CONTEXT_EXPIRE_DAYS", 30))

    ADMIN_ID = os.getenv("ADMIN_ID")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

    # ID создателя (папы) — для пасхалок
    CREATOR_IDS = [
        int(os.getenv("CREATOR_ID_1", "1928090839")),
        int(os.getenv("CREATOR_ID_2", "1912340181")),
    ]

    # Пути
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    AUDIO_DIR = DATA_DIR / "audio"

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    CONVERSATIONS_DB = DATA_DIR / "conversations.db"
    REMINDERS_DB = DATA_DIR / "reminders.db"
