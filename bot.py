import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler

API_URL = "https://tarotdiana.up.railway.app/api/tarot"
TOKEN = "8110406311:AAGXqdLT19zdw9-77lLLCP9gy0UeI4IUXgk"

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

    interpretation = data["interpretation"]
    cards = data["cards"]

    images = []
    for card in cards:
        url = f"https://tarotdiana.up.railway.app/static/tarot/{card['filename']}"
        if card["reversed"]:
            url += "?reversed"  # просто для наглядности
        images.append(url)

    # Отправляем картинки
    for url in images:
        await query.message.reply_photo(url)

    # Отправляем толкование
    await query.message.reply_text(f"🧙‍♀️ Толкование:\n\n{interpretation}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_mode_selection))

    print("Бот запущен. Жми Ctrl+C чтобы остановить.")
    app.run_polling()
