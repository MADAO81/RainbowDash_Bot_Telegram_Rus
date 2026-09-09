"""
Планировщик для бота Рэйнбоу Дэш.
Отправка бодрого старта в 8:45 и рок-рекомендации в 17:45.

Автор: MADAO81
Версия: 2.1 — исправлен формат рок-рекомендации
"""

import logging
import sqlite3
import random
from telegram import Update
from telegram.ext import ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.config import Config
from bot.services.ai_service import get_morning_start, get_rainbow_response

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
DB_PATH = Config.DATA_DIR / "subscriptions.db"
ROCK_DB_PATH = Config.DATA_DIR / "rock_songs.db"


def _get_connection():
    return sqlite3.connect(DB_PATH)


def _init_db():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            chat_id INTEGER PRIMARY KEY,
            subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_chat(chat_id: int):
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subscriptions (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()
    logger.info(f"📋 Чат {chat_id} добавлен для рассылки")


def remove_chat(chat_id: int):
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()
    logger.info(f"📋 Чат {chat_id} удалён из рассылки")


def get_active_chats():
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM subscriptions")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def get_random_song():
    """Возвращает случайную песню из БД."""
    conn = sqlite3.connect(ROCK_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT artist, song, vibe FROM rock_songs ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"artist": row[0], "song": row[1], "vibe": row[2]}
    return None


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    add_chat(chat_id)
    await update.message.reply_text(
        "🌈 *Ты подписался на ежедневные рассылки Рэйнбоу Дэш!*\n\n"
        "⚡ Каждый день в 8:45 я буду присылать тебе бодрый старт!\n"
        "🎸 А в 17:45 — рок-рекомендацию!\n\n"
        "Чтобы отписаться, напиши /unsubscribe 😢",
        parse_mode="Markdown"
    )


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    remove_chat(chat_id)
    await update.message.reply_text(
        "😢 *Ты отписался от рассылок!*\n\n"
        "Если захочешь вернуться — напиши /subscribe 🌈",
        parse_mode="Markdown"
    )


async def send_long_message(bot, chat_id: int, text: str, parse_mode: str = "Markdown"):
    if not text:
        return

    if len(text) < 4000:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
        return

    parts = []
    current_part = ""
    for paragraph in text.split('\n'):
        if len(current_part) + len(paragraph) + 1 < 4000:
            current_part += paragraph + '\n'
        else:
            if current_part:
                parts.append(current_part.strip())
            current_part = paragraph + '\n'
    if current_part:
        parts.append(current_part.strip())

    if len(parts) == 1 and len(parts[0]) > 4000:
        words = parts[0].split()
        parts = []
        current_part = ""
        for word in words:
            if len(current_part) + len(word) + 1 < 4000:
                current_part += word + ' '
            else:
                parts.append(current_part.strip())
                current_part = word + ' '
        if current_part:
            parts.append(current_part.strip())

    for i, part in enumerate(parts):
        if i == 0:
            await bot.send_message(chat_id=chat_id, text=part, parse_mode=parse_mode)
        else:
            await bot.send_message(chat_id=chat_id, text=f"*Продолжение:*\n{part}", parse_mode="Markdown")


async def send_morning_start(app):
    active_chats = get_active_chats()
    if not active_chats:
        logger.info("📭 Нет активных чатов для бодрого старта")
        return

    logger.info(f"⚡ Отправка бодрого старта в {len(active_chats)} чатов...")

    message = await get_morning_start()
    if not message:
        message = "⚡ *Бодрый старт!* Вжух — и новый день твой! Не тормози! 🌈"

    for chat_id in active_chats:
        try:
            await send_long_message(app.bot, chat_id, message, parse_mode="Markdown")
            logger.info(f"✅ Бодрый старт отправлен в чат {chat_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки в чат {chat_id}: {e}")
            if "bot was blocked" in str(e) or "chat not found" in str(e):
                remove_chat(chat_id)


async def send_evening_rock(app):
    active_chats = get_active_chats()
    if not active_chats:
        logger.info("📭 Нет активных чатов для рок-рекомендации")
        return

    logger.info(f"🎸 Отправка рок-рекомендации в {len(active_chats)} чатов...")

    # Берём случайную песню из БД
    song = get_random_song()
    if not song:
        logger.warning("⚠️ Нет песен в базе данных!")
        return

    artist = song['artist']
    song_title = song['song']
    vibe = song.get('vibe', '')

    # Формируем запрос к DeepSeek для переработки в стиле Радуги
    prompt = f"""
Ты — Рэйнбоу Дэш, энергичная и дерзкая пони из Понивилля. 

Сейчас ты делаешь рок-рекомендацию в ежедневной рассылке. Тебе нужно написать сообщение для фанатов рока.

Вот песня, которую ты выбрала:
- Исполнитель: {artist}
- Название: "{song_title}"
- Настроение/стиль: {vibe if vibe else 'рок'}

Твоя задача — написать яркое, короткое сообщение (2-4 предложения) по этому шаблону:

🎸 *{artist} — «{song_title}»*

[Твой энергичный комментарий о песне: почему она крутая, какие эмоции вызывает, что в ней особенного. Говори как Рэйнбоу Дэш — дерзко, с драйвом, используй эмодзи ⚡🎸🤘🔥]

ВАЖНО:
1. Начинай с заголовка: "🎸 *{artist} — «{song_title}»*"
2. После заголовка — твой комментарий
3. Используй Markdown для заголовка
4. Коротко и энергично!
"""
    message = await get_rainbow_response(prompt)
    
    # Если AI не ответил — формируем сообщение самостоятельно
    if not message:
        vibe_text = f" ({vibe})" if vibe else ""
        message = f"🎸 *{artist} — «{song_title}»*{vibe_text}\n\nВрубай на полную! Эта песня — чистый адреналин! 🤘⚡"

    for chat_id in active_chats:
        try:
            await send_long_message(app.bot, chat_id, message, parse_mode="Markdown")
            logger.info(f"✅ Рок-рекомендация отправлена в чат {chat_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки в чат {chat_id}: {e}")
            if "bot was blocked" in str(e) or "chat not found" in str(e):
                remove_chat(chat_id)


def start_scheduler(app):
    try:
        _init_db()

        default_chats = getattr(Config, 'DEFAULT_CHATS', "")
        if default_chats:
            for chat_id in default_chats.split(","):
                try:
                    chat_id = int(chat_id.strip())
                    add_chat(chat_id)
                    logger.info(f"✅ Автоматически добавлен чат: {chat_id}")
                except Exception as e:
                    logger.error(f"❌ Ошибка добавления чата {chat_id}: {e}")

        scheduler.add_job(
            send_morning_start,
            CronTrigger(hour=8, minute=45),
            args=[app],
            id='morning_start',
            replace_existing=True
        )

        scheduler.add_job(
            send_evening_rock,
            CronTrigger(hour=17, minute=45),
            args=[app],
            id='evening_rock',
            replace_existing=True
        )

        scheduler.start()
        logger.info("✅ Планировщик Рэйнбоу Дэш запущен. Бодрый старт в 8:45, рок в 17:45")

    except Exception as e:
        logger.error(f"❌ Ошибка при запуске планировщика: {e}")


def stop_scheduler():
    try:
        scheduler.shutdown()
        logger.info("⏹️ Планировщик остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка при остановке планировщика: {e}")
