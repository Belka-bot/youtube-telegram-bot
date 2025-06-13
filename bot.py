import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp

# 8043979489:AAHau-aJHv6ZmXkHdSgQq2iM4TVfQx6DbvQ ОТ BotFather
TOKEN = '8043979489:AAHau-aJHv6ZmXkHdSgQq2iM4TVfQx6DbvQ'

def is_youtube_url(text):
    return 'youtube.com/watch' in text or 'youtu.be/' in text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    if is_youtube_url(message_text):
        keyboard = [
            [InlineKeyboardButton("🔽 Скачать видео", callback_data=message_text)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Видео обнаружено. Нажми кнопку для скачивания:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    url = query.data

    await query.edit_message_text("🎥 Скачиваю видео...")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
        'noplaylist': True,
        'quiet': True,
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
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ Бот запущен.")
    app.run_polling()

if __name__ == '__main__':
    main()
