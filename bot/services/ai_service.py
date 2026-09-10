"""
AI сервис для бота Рэйнбоу Дэш (DeepSeek + OpenAI).

Автор: MADAO81
Версия: 1.3 — утренняя рассылка через полноценный диалог (фикс обрезания)
"""

import logging
import base64
import os
import time
from pathlib import Path
from typing import Optional, List, Dict
from openai import AsyncOpenAI
from bot.config import Config
from bot.core.constants import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


# === DEEPSEEK ДЛЯ ТЕКСТА ===
async def get_rainbow_response(
    user_message: str,
    mood_description: str = "happy",
    context_history: Optional[List[Dict]] = None
) -> Optional[str]:
    """Генерирует ответ от Рэйнбоу Дэш через DeepSeek."""
    try:
        client = AsyncOpenAI(
            api_key=Config.PROXY_API_KEY,
            base_url="https://api.proxyapi.ru/openrouter/v1"
        )

        system_prompt = SYSTEM_PROMPT

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Your current mood is: {mood_description}"}
        ]

        if context_history:
            messages.extend(context_history[-10:])

        messages.append({"role": "user", "content": user_message})

        response = await client.chat.completions.create(
            model=Config.DEEPSEEK_MODEL,
            messages=messages,
            max_tokens=Config.DEEPSEEK_MAX_TOKENS,
            temperature=Config.DEEPSEEK_TEMPERATURE,
            timeout=30.0
        )

        if response.choices and len(response.choices) > 0:
            choice = response.choices[0]
            finish_reason = choice.finish_reason
            content = choice.message.content.strip() if choice.message.content else None

            if finish_reason == "length":
                logger.warning(f"⚠️ Ответ обрезан по длине! content_length={len(content) if content else 0}")
            else:
                logger.debug(f"✅ Ответ получен. finish_reason={finish_reason}")

            return content
        return None

    except Exception as e:
        logger.error(f"❌ DeepSeek error: {e}")
        return None


# === РАССЫЛКИ ===
async def get_morning_start() -> Optional[str]:
    """
    Генерирует бодрое утреннее сообщение.
    Использует тот же механизм, что и личный диалог, чтобы избежать обрезания.
    """
    # Промпт в стиле диалога — как будто пользователь просит написать сообщение
    user_message = (
        "Представь, что ты пишешь сообщение в чат для своих подписчиков. "
        "Это НЕ команда, а полноценное утреннее приветствие. "
        "Напиши развёрнутое бодрое сообщение: поздоровайся, разбуди, замотивируй, пожелай хорошего дня. "
        "ОБЯЗАТЕЛЬНО на русском языке. Говори как Рэйнбоу Дэш — дерзко, с драйвом, энергично. "
        "Сообщение должно быть ЗАКОНЧЕННЫМ — с началом, основной частью и концовкой. "
        "НЕ обрывай на полуслове. НЕ пиши коротко. Пиши как будто рассказываешь другу."
    )

    logger.info("🌅 Генерация утреннего сообщения через get_rainbow_response...")
    return await get_rainbow_response(user_message, mood_description="happy")


async def get_evening_rock() -> Optional[str]:
    """
    Генерирует вечернюю рок-рекомендацию.
    Использует тот же механизм, что и личный диалог.
    """
    user_message = (
        "Представь, что ты пишешь вечернее сообщение в чат для подписчиков. "
        "Расскажи о рок-музыке или дай совет по спорту на вечер. "
        "ОБЯЗАТЕЛЬНО на русском языке. Говори как Рэйнбоу Дэш. "
        "Сообщение должно быть законченным и развёрнутым."
    )

    logger.info("🎸 Генерация вечернего сообщения через get_rainbow_response...")
    return await get_rainbow_response(user_message, mood_description="happy")


# === OPENAI ДЛЯ ГОЛОСА ===
async def transcribe_audio(
    audio_data: bytes,
    file_extension: str = ".ogg"
) -> Optional[str]:
    """Транскрибирует аудио через OpenAI Whisper."""
    try:
        client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)

        audio_dir = Path(Config.AUDIO_DIR)
        audio_dir.mkdir(parents=True, exist_ok=True)

        audio_path = audio_dir / f"voice_{int(time.time())}{file_extension}"
        with open(audio_path, "wb") as f:
            f.write(audio_data)

        with open(audio_path, "rb") as audio_file:
            transcription = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ru"
            )

        os.remove(audio_path)

        if transcription and transcription.text:
            return transcription.text.strip()
        return None

    except Exception as e:
        logger.error(f"❌ Whisper error: {e}")
        return None
