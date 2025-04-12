
from flask import Flask, render_template, request
from utils.tarot_logic import select_cards, generate_interpretation, get_random_bun_message, TAROT_CARDS
import random

app = Flask(__name__)

@app.route("/api/tarot", methods=["POST"])
def api_tarot():
    data = request.json or {}
    mode = data.get("mode", "м")
    cards = select_cards(TAROT_CARDS)
    interpretation = generate_interpretation(cards, mode)
    result = {
        "cards": cards,
        "interpretation": interpretation
    }
   

@app.route("/", methods=["GET", "POST"])
def index():
    mode = request.form.get("mode", "м")
    cards = select_cards(TAROT_CARDS)
    interpretation = generate_interpretation(cards, mode)
    spell_message = get_spell_message()
    bun_message = get_random_bun_message()

    return render_template("index.html",
                           cards=cards,
                           interpretation=interpretation,
                           spell_message=spell_message,
                           bun_message=bun_message,
                           mode=mode)

def get_spell_message():
    return random.choice([
        "Ты — свет в этом мире 🌟",
        "Каждая карта — шаг к себе ✨",
        "Магия уже рядом. Просто доверься 🌌",
        "Душа знает путь, а карты подсказывают направление 🔮",
        "Ты не одна — звёзды с тобой 🌙"
    ])

if __name__ == "__main__":
    app.run(debug=True)
