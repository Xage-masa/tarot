
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from utils.tarot_logic import select_cards, generate_interpretation, get_random_bun_message, TAROT_CARDS
import random

app = Flask(__name__)
app.secret_key = "my_mystical_secret"

# Texts for different languages
TEXTS = {
    "ru": {
        "spell_messages": [
            "Ты — свет в этом мире 🌟",
            "Каждая карта — шаг к себе ✨",
            "Магия уже рядом. Просто доверься 🌌",
            "Душа знает путь, а карты подсказывают направление 🔮",
            "Ты не одна — звёзды с тобой 🌙"
        ],
        "default_mode": "м"
    },
    "tr": {
        "spell_messages": [
            "Sen bu dünyada bir ışıksın 🌟",
            "Her kart kendine atılan bir adım ✨",
            "Büyü zaten yakınlarda. Sadece güven 🌌",
            "Ruh yolunu biliyor, kartlar ise yönü gösteriyor 🔮",
            "Yalnız değilsin — yıldızlar seninle 🌙"
        ],
        "default_mode": "m"
    },
    "en": {
        "spell_messages": [
            "You are a light in this world 🌟",
            "Every card is a step to yourself ✨",
            "Magic is near. Just trust it 🌌",
            "The soul knows the way, the cards reveal the path 🔮",
            "You are not alone — the stars are with you 🌙"
        ],
        "default_mode": "m"
    }
}

@app.route("/set_language/<lang>")
def set_language(lang):
    if lang in TEXTS:
        session['lang'] = lang
    return redirect(url_for("index"))

@app.route("/api/tarot", methods=["POST"])
def api_tarot():
    lang = session.get('lang', 'ru')
    data = request.json or {}
    mode = data.get("mode", TEXTS[lang]["default_mode"])
    cards = select_cards(TAROT_CARDS)
    interpretation = generate_interpretation(cards, mode)
    result = {
        "cards": cards,
        "interpretation": interpretation
    }
    return jsonify(result)

@app.route("/", methods=["GET", "POST"])
def index():
    lang = session.get('lang', 'ru')
    mode = request.form.get("mode", TEXTS[lang]["default_mode"])
    cards = select_cards(TAROT_CARDS)
    interpretation = generate_interpretation(cards, mode)
    spell_message = random.choice(TEXTS[lang]['spell_messages'])
    bun_message = get_random_bun_message()

    return render_template("index.html",
                           cards=cards,
                           interpretation=interpretation,
                           spell_message=spell_message,
                           bun_message=bun_message,
                           mode=mode,
                           lang=lang)

if __name__ == "__main__":
    app.run(debug=True)
