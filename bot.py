import os
import logging
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем токен
TOKEN = os.environ["TOKEN"]

# Функция загрузки
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'noplaylist': True,
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        },
        # Если понадобится — раскомментируй и подставь свой proxy:
        # 'proxy': 'socks5://user:pass@host:port',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь ссылку на видео — я постараюсь её скачать.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.effective_chat.id
    await update.message.reply_text("Скачиваю видео…")
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, download_video, url)
        with open("video.mp4", "rb") as f:
            await context.bot.send_video(chat_id=chat_id, video=f)
        os.remove("video.mp4")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при скачивании: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if name == "main":
    main()
