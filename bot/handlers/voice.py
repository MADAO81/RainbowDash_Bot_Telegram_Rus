import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import transcribe_audio
from bot.services.ai_service import get_rainbow_response
from bot.utils.time_utils import is_working_hours
from bot.core.context_manager import ContextManager

logger = logging.getLogger(__name__)
context_manager = ContextManager()

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_working_hours():
        return

    status_message = await update.message.reply_text("🎧 Слушаю...")

    try:
        user_id = update.effective_user.id
        voice = update.message.voice
        file = await voice.get_file()
        audio_data = await file.download_as_bytearray()

        transcript = await transcribe_audio(audio_data, ".ogg")
        if not transcript:
            await status_message.edit_text("😅 Не разобрала! Говори чётче! 🌈")
            return

        context_history = context_manager.get_context(user_id)
        response = await get_rainbow_response(
            user_message=transcript,
            mood_description="happy",
            context_history=context_history
        )

        if not response:
            response = "⚡ Вжух! Что-то я задумалась... Давай ещё раз! 🌈"

        await status_message.delete()
        await update.message.reply_text(f"🎤 *Ты сказал:* _{transcript[:100]}..._\n\n{response}", parse_mode="Markdown")
        context_manager.save_context(user_id, transcript, response)

    except Exception as e:
        logger.error(f"❌ Voice error: {e}")
        await status_message.edit_text("😅 Ошибка! Попробуй ещё раз! 🌈")
