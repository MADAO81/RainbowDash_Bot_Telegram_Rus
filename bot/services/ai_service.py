"""
AI сервис для бота Рэйнбоу Дэш (DeepSeek + OpenAI).

Автор: MADAO81
Версия: 1.0
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
            return response.choices[0].message.content.strip()
        return None

    except Exception as e:
        logger.error(f"❌ DeepSeek error: {e}")
        return None


# === РАССЫЛКИ ===
async def get_morning_start() -> Optional[str]:
    """Генерирует бодрое утреннее сообщение на РУССКОМ языке."""
    try:
        client = AsyncOpenAI(
            api_key=Config.PROXY_API_KEY,
            base_url="https://api.proxyapi.ru/openrouter/v1"
        )

        prompt = "Придумай короткую, энергичную и мотивирующую фразу для начала дня. ОБЯЗАТЕЛЬНО на русском языке. Говори как Рэйнбоу Дэш — дерзко, с драйвом."
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        response = await client.chat.completions.create(
            model=Config.DEEPSEEK_MODEL,
            messages=messages,
            max_tokens=200,
            temperature=0.9,
            timeout=30.0
        )

        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        return None

    except Exception as e:
        logger.error(f"❌ Morning start error: {e}")
        return None


async def get_evening_rock() -> Optional[str]:
    """Генерирует вечернюю рок-рекомендацию на РУССКОМ языке."""
    try:
        client = AsyncOpenAI(
            api_key=Config.PROXY_API_KEY,
            base_url="https://api.proxyapi.ru/openrouter/v1"
        )

        prompt = "Предложи короткую рекомендацию по рок-музыке или спорту для вечера. ОБЯЗАТЕЛЬНО на русском языке. Говори как Рэйнбоу Дэш."
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        response = await client.chat.completions.create(
            model=Config.DEEPSEEK_MODEL,
            messages=messages,
            max_tokens=250,
            temperature=0.9,
            timeout=30.0
        )

        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        return None

    except Exception as e:
        logger.error(f"❌ Evening rock error: {e}")
        return None


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
