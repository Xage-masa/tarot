import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
import requests

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "https://tarotdiana.up.railway.app/api/tarot"

MODES = {
    "Общий": "м",
    "Любовь": "ж",
    "На завтра": "д"
}

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for name, code in MODES.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери тип расклада:", reply_markup=reply_markup)

async def handle_mode_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    mode = query.data

    response = requests.get(API_URL, params={"mode": mode})
    data = response.json()

    cards_text = "\n".join([f"🔮 {card['name']}" for card in data["cards"]])
    interpretation = data["interpretation"]

    await query.message.reply_text(f"{cards_text}\n\n📝 Расшифровка:\n{interpretation}")

# 💡 Вот эта функция нужна app.py
def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_mode_selection))
    application.run_polling()
