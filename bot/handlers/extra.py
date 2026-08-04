"""
Дополнительные команды для бота Рэйнбоу Дэш.
Команды: /sport, /rock, /harley, /challenge, /motivate, /truth

Автор: MADAO81
Версия: 1.0
"""

import logging
import random
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import get_rainbow_response
from bot.utils.time_utils import is_working_hours, get_working_status_message

logger = logging.getLogger(__name__)

# === FALLBACK-ОТВЕТЫ ===
FALLBACK_SPORT = [
    "💪 *Спорт — это круто!* Начни с 10 отжиманий прямо сейчас! Вжух!",
    "💪 *Сегодня — день рекордов!* Пробеги 1 км и докажи, что ты не тормоз!",
]

FALLBACK_ROCK = [
    "🎸 *Рок жив!* Послушай AC/DC — это всегда заряжает! 🤘",
    "🎸 *Вруби металл!* Metallica — лучший выбор для вечера!",
]

FALLBACK_HARLEY = [
    "🏍️ *Harley Davidson — это свобода!* Первый мотоцикл был создан в 1903 году!",
    "🏍️ *Harley — это не просто байк, это образ жизни!*",
]

FALLBACK_CHALLENGE = [
    "⚡ *Слабо отжаться 20 раз?* Давай, покажи, на что способен!",
    "⚡ *Бросаю тебе вызов!* Сделай 10 бёрпи прямо сейчас!",
]

FALLBACK_MOTIVATE = [
    "🤘 *Ты можешь больше, чем думаешь!* Вжух — и победа за тобой!",
    "🤘 *Не сдавайся!* Даже если трудно — ты крутой!",
]

FALLBACK_TRUTH = [
    "🗣️ *Честно скажу:* Ты — крутой, но мог бы быть ещё круче!",
    "🗣️ *Правда:* Скорость — это жизнь. Не тормози!",
]


async def _get_fallback(command_type: str) -> str:
    fallbacks = {
        'sport': FALLBACK_SPORT,
        'rock': FALLBACK_ROCK,
        'harley': FALLBACK_HARLEY,
        'challenge': FALLBACK_CHALLENGE,
        'motivate': FALLBACK_MOTIVATE,
        'truth': FALLBACK_TRUTH,
    }
    return random.choice(fallbacks.get(command_type, FALLBACK_SPORT))


async def sport_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    args = context.args
    query = " ".join(args) if args else "спорт"

    status_message = await update.message.reply_text("💪 Дай-ка подумать...")

    try:
        response = await get_rainbow_response(
            user_message=f"Пользователь просит совет по спорту: {query}. Дай короткий, энергичный совет. Говори как Рэйнбоу Дэш.",
            mood_description="happy"
        )

        await status_message.delete()
        if response:
            await update.message.reply_text(f"💪 *Совет от Рэйнбоу Дэш:*\n\n{response}", parse_mode="Markdown")
        else:
            await update.message.reply_text(await _get_fallback('sport'), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"❌ Sport error: {e}")
        await status_message.edit_text(await _get_fallback('sport'), parse_mode="Markdown")


async def rock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    args = context.args
    query = " ".join(args) if args else "рок"

    status_message = await update.message.reply_text("🎸 Сейчас найду что-то крутое...")

    try:
        response = await get_rainbow_response(
            user_message=f"Пользователь просит рок-рекомендацию: {query}. Предложи песню или исполнителя. Говори как Рэйнбоу Дэш.",
            mood_description="happy"
        )

        await status_message.delete()
        if response:
            await update.message.reply_text(f"🎸 *Рок-рекомендация:*\n\n{response}", parse_mode="Markdown")
        else:
            await update.message.reply_text(await _get_fallback('rock'), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"❌ Rock error: {e}")
        await status_message.edit_text(await _get_fallback('rock'), parse_mode="Markdown")


async def harley_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    args = context.args
    query = " ".join(args) if args else "Harley Davidson"

    status_message = await update.message.reply_text("🏍️ Сейчас расскажу что-то крутое...")

    try:
        response = await get_rainbow_response(
            user_message=f"Пользователь просит факт о Harley Davidson: {query}. Расскажи интересный факт. Говори как Рэйнбоу Дэш.",
            mood_description="happy"
        )

        await status_message.delete()
        if response:
            await update.message.reply_text(f"🏍️ *Факт о Harley Davidson:*\n\n{response}", parse_mode="Markdown")
        else:
            await update.message.reply_text(await _get_fallback('harley'), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"❌ Harley error: {e}")
        await status_message.edit_text(await _get_fallback('harley'), parse_mode="Markdown")


async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("⚡ Сейчас я брошу тебе вызов...")

    try:
        response = await get_rainbow_response(
            user_message="Брось пользователю вызов — предложи сделать физическое упражнение (отжимания, приседания, бёрпи) или небольшое достижение. Говори как Рэйнбоу Дэш.",
            mood_description="happy"
        )

        await status_message.delete()
        if response:
            await update.message.reply_text(f"⚡ *Вызов от Рэйнбоу Дэш:*\n\n{response}", parse_mode="Markdown")
        else:
            await update.message.reply_text(await _get_fallback('challenge'), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"❌ Challenge error: {e}")
        await status_message.edit_text(await _get_fallback('challenge'), parse_mode="Markdown")


async def motivate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("🤘 Сейчас я тебя подбодрю...")

    try:
        response = await get_rainbow_response(
            user_message="Скажи пользователю что-то мотивирующее и энергичное. Говори как Рэйнбоу Дэш.",
            mood_description="happy"
        )

        await status_message.delete()
        if response:
            await update.message.reply_text(f"🤘 *Слова поддержки:*\n\n{response}", parse_mode="Markdown")
        else:
            await update.message.reply_text(await _get_fallback('motivate'), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"❌ Motivate error: {e}")
        await status_message.edit_text(await _get_fallback('motivate'), parse_mode="Markdown")


async def truth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("🗣️ Сейчас я скажу правду...")

    try:
        response = await get_rainbow_response(
            user_message="Скажи честную, прямую фразу о жизни или человеке. Говори как Рэйнбоу Дэш.",
            mood_description="happy"
        )

        await status_message.delete()
        if response:
            await update.message.reply_text(f"🗣️ *Правда от Рэйнбоу Дэш:*\n\n{response}", parse_mode="Markdown")
        else:
            await update.message.reply_text(await _get_fallback('truth'), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"❌ Truth error: {e}")
        await status_message.edit_text(await _get_fallback('truth'), parse_mode="Markdown")
