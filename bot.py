import os
import logging
import yt_dlp
import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
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
       'merge_output_format' : 'mp4' ,
        'noplaylist': True,
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        },
        'cookiefile': 'cookies.txt',  # ← Вот это добавь
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь ссылку на YouTube-видео, и я его скачаю!")

# Обработка видео-ссылок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.effective_chat.id

    try:
        await update.message.reply_text("Скачиваю видео...")
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download_youtube_video, url)

        with open("video.mp4", "rb") as video:
            await context.bot.send_video(chat_id=chat_id, video=video)

        os.remove("video.mp4")

    except Exception as e:
        await update.message.reply_text(f"Ошибка при скачивании: {e}")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
