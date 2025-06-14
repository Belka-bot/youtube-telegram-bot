import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

TOKEN = os.environ["TOKEN"]

def download_youtube_video(url, chat_id):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{chat_id}_{int(time.time())}.mp4',
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        },
        'cookiefile': 'cookies.txt'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь ссылку на YouTube-видео, и я его скачаю!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.effective_chat.id
    file_name = f'{chat_id}_{int(time.time())}.mp4'
    download_youtube_video(url, chat_id)
    if os.path.exists(file_name):
        await context.bot.send_video(chat_id=chat_id, video=open(file_name, 'rb'))
        os.remove(file_name)
    else:
        await context.bot.send_message(chat_id=chat_id, text="Ошибка при скачивании видео.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

