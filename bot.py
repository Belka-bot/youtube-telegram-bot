import os
import logging
import yt_dlp
import asyncio

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Включаем логирование

logging.basicConfig(level=logging.INFO)

# Получаем токен из переменной окружения

TOKEN = os.environ["TOKEN"]

# Функция загрузки видео

def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'noplaylist': True,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Привет! Отправь ссылку на YouTube-видео, чтобы я скачал его для тебя.")

# Обработка текстовых сообщений

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.effective_chat.id
    try:
        await update.message.reply_text("Скачиваю видео...")
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download_youtube_video, url)
        await context.bot.send_video(chat_id=chat_id, video=open("video.mp4", "rb"))
        os.remove("video.mp4")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при скачивании: {e}")

# Обработка кнопок (если вдруг появятся в будущем)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.callback_query.answer() await update.callback_query.edit_message_text("Кнопка нажата!")

# Основная функция запуска

def main(): app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(button_callback))

print("✅ Бот запущен.")
app.run_polling()

if name == "main": main()
