import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ["TOKEN"]

def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.mp4',
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        },
        'cookiefile': 'cookies.txt'
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь ссылку на YouTube-видео, и я его скачаю!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.effective_chat.id
    await update.message.reply_text("Скачиваю видео...")
    try:
        download_youtube_video(url)
        await context.bot.send_video(chat_id=chat_id, video=open("video.mp4", "rb"))
    except Exception as e:
        await update.message.reply_text(f"Ошибка при скачивании: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
