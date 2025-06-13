import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp

TOKEN = 
"8043979489:AAEb8ydxUhSlWZpheyXM83vA_Qc0T8U25Uw"

def is_youtube_url(text):
    return 'youtube.com/watch' in text or 'youtu.be/' in text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'force_ipv4': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await context.bot.send_video(chat_id=update.effective_chat.id, video=open('video.mp4', 'rb'))
        os.remove('video.mp4')
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"⚠️ Ошибка: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Отправь ссылку на YouTube-видео, чтобы скачать его!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен.")
    app.run_polling()

if __name__ == '__main__':
    main()
