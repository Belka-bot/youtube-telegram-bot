import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
from yt_dlp import YoutubeDL

TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь ссылку на YouTube-видео, и я его скачаю с выбором качества!")

def build_keyboard(formats):
    buttons = [
        [InlineKeyboardButton(f"{f['format']} — {f['resolution']} ({f['filesize']} MB)", callback_data=f["format_id"])]
        for f in formats
    ]
    return InlineKeyboardMarkup(buttons)

def get_video_formats(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'cookiefile': 'cookies.txt',
        'forcejson': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = []
        for f in info.get("formats", []):
            if f.get("vcodec") != "none" and f.get("acodec") != "none":
                size_mb = round(f.get("filesize", 0) / 1024 / 1024, 1) if f.get("filesize") else '?'
                formats.append({
                    "format": f.get("format_note") or f.get("ext"),
                    "resolution": f.get("resolution") or f.get("height", ''),
                    "filesize": size_mb,
                    "format_id": f.get("format_id")
                })
        return formats, info.get("id")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    formats, video_id = get_video_formats(url)
    context.user_data["url"] = url
    context.user_data["video_id"] = video_id
    await update.message.reply_text("Выбери качество:", reply_markup=build_keyboard(formats))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    fmt = query.data
    url = context.user_data["url"]
    video_id = context.user_data["video_id"]
    filename = f"{video_id}_{fmt}_{int(time.time())}.mp4"

    ydl_opts = {
        'format': fmt,
        'outtmpl': filename,
        'merge_output_format': 'mp4',
        'cookiefile': 'cookies.txt',
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    with open(filename, 'rb') as f:
        await query.message.reply_video(video=f)

    os.remove(filename)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
