
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from utils.tarot_logic import select_cards, generate_interpretation, get_random_bun_message, TAROT_CARDS
import random

app = Flask(__name__)
app.secret_key = "my_mystical_secret"

# Texts for different languages
TEXTS = {
    "ru": {
        "default_mode": "м",
        "ui": {
            "title": "🔮 Волшебные предсказания от Дианочки",
            "toggle_theme": "Переключить стиль",
            "get_layout": "Получить расклад 🔮",
            "type_layout": "🎇 Тип расклада:"
        },
        "spell_messages": [
            "Ты — свет в этом мире 🌟",
            "Каждая карта — шаг к себе ✨",
            "Магия уже рядом. Просто доверься 🌌",
            "Душа знает путь, а карты подсказывают направление 🔮",
            "Ты не одна — звёзды с тобой 🌙"
        ],
        "spread_types": {
            "м": "Общий",
            "ж": "Любовный",
            "д": "На день",
            "дв": "Друзья / Враги",
            "б": "Будущее",
            "н": "Да / Нет"
        },
        "bun_messages": {
            "м": [
                "🔮 Всё в твоих руках. Прислушайся к себе.",
                "🧘 Иногда — не делать ничего, уже действие.",
                "🌌 Не забывай, что ты — космос в теле."
            ],
            "ж": [
                "💖 Любовь приходит к тем, кто открыт и спокоен.",
                "🥐 Ты достойна заботы, и не только от других.",
                "🫶 Не бойся быть уязвимой — в этом сила."
            ],
            "д": [
                "☀️ Начни день с улыбки — и магия подтянется.",
                "🔋 Сохрани энергию для того, что важно.",
                "🍃 Пусть этот день принесет ясность."
            ],
            "дв": [
                "🎭 Не все друзья — друзья. Присмотрись.",
                "🤝 Иногда враг — это урок, замаскированный под человека.",
                "🧿 Доверяй, но проверяй."
            ],
            "б": [
                "🔮 Будущее не написано — ты автор.",
                "🚀 Всё возможно, если ты в это веришь.",
                "🧭 Дорога сама покажет путь."
            ],
            "н": [
                "🙈 Иногда неважно да или нет — важно спросить себя почему.",
                "🪞 Ответ уже внутри тебя.",
                "🎲 Жизнь — игра, и ты бросаешь кубик."
            ]
        }
    },
    "tr": {
        "default_mode": "m",
        "ui": {
            "title": "🔮 Diana'nın Büyülü Kehanetleri",
            "toggle_theme": "Temayı Değiştir",
            "get_layout": "Kart Açılımı Al 🔮",
            "type_layout": "🎇 Açılım Tipi:"
        },
        "spell_messages": [
            "Sen bu dünyada bir ışıksın 🌟",
            "Her kart kendine atılan bir adım ✨",
            "Büyü zaten yakınlarda. Sadece güven 🌌",
            "Ruh yolunu biliyor, kartlar ise yönü gösteriyor 🔮",
            "Yalnız değilsin — yıldızlar seninle 🌙"
        ],
        "spread_types": {
            "м": "Genel",
            "ж": "Aşk",
            "д": "Günlük",
            "дв": "Dost / Düşman",
            "б": "Gelecek",
            "н": "Evet / Hayır"
        },
        "bun_messages": {
            "м": [
                "🔮 Her şey senin ellerinde. İç sesini dinle.",
                "🧘 Bazen hiçbir şey yapmamak da bir eylemdir.",
                "🌌 Unutma, sen evrensin, sadece küçücük bir bedende."
            ],
            "ж": [
                "💖 Aşk, kalbi açık olana gelir.",
                "🥐 İlgiye değersin — sadece başkalarından değil.",
                "🫶 Kırılganlıkta da bir güç vardır. Korkma."
            ],
            "д": [
                "☀️ Gülümseyerek başla — sihir peşinden gelir.",
                "🔋 Gücünü önemlilere sakla.",
                "🍃 Bugün sana berraklık getirsin."
            ],
            "дв": [
                "🎭 Her dost, dost değildir. Dikkat et.",
                "🤝 Düşman bazen kılık değiştirmiş bir öğretmendir.",
                "🧿 Güven ama kontrol et."
            ],
            "б": [
                "🔮 Gelecek yazılmamış — kalem senin elinde.",
                "🚀 İnandığında her şey mümkündür.",
                "🧭 Yol seni bulacaktır."
            ],
            "н": [
                "🙈 Evet mi hayır mı değil, neden diye sormalı.",
                "🪞 Cevap zaten içinde.",
                "🎲 Hayat bir oyun, zar senin elinde."
            ]
        }
    },
    "en": {
        "default_mode": "m",
        "ui": {
            "title": "🔮 Magical Predictions by Diana",
            "toggle_theme": "Toggle Theme",
            "get_layout": "Get Spread 🔮",
            "type_layout": "🎇 Spread Type:"
        },
        "spell_messages": [
            "You are a light in this world 🌟",
            "Every card is a step to yourself ✨",
            "Magic is near. Just trust it 🌌",
            "The soul knows the way, the cards reveal the path 🔮",
            "You are not alone — the stars are with you 🌙"
        ],
        "spread_types": {
            "м": "General",
            "ж": "Love",
            "д": "Daily",
            "дв": "Friends / Foes",
            "б": "Future",
            "н": "Yes / No"
        },
        "bun_messages": {
            "м": [
                "🔮 Everything is in your hands. Listen to yourself.",
                "🧘 Sometimes doing nothing is still doing something.",
                "🌌 Don't forget — you are the universe in a body."
            ],
            "ж": [
                "💖 Love comes to those who stay soft and open.",
                "🥐 You are worthy of care — not just from others.",
                "🫶 Don’t fear vulnerability. That’s where strength lives."
            ],
            "д": [
                "☀️ Start the day with a smile — magic will follow.",
                "🔋 Save your energy for what matters.",
                "🍃 May this day bring you clarity."
            ],
            "дв": [
                "🎭 Not every friend is a friend. Look closer.",
                "🤝 Sometimes the enemy is a lesson in disguise.",
                "🧿 Trust, but verify."
            ],
            "б": [
                "🔮 The future is unwritten — and you hold the pen.",
                "🚀 Everything is possible if you believe it.",
                "🧭 The path will reveal itself."
            ],
            "н": [
                "🙈 Sometimes the question isn’t yes or no — it’s why.",
                "🪞 The answer is already within you.",
                "🎲 Life is a game, and you're rolling the dice."
            ]
        }
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
    interpretation = generate_interpretation(cards, mode, lang)
    result = {
        "cards": cards,
        "interpretation": interpretation
    }
    return jsonify(result)

@app.route("/", methods=["GET", "POST"])
def index():
    # Берём язык из сессии
    lang = session.get('lang', 'ru')

    # Добавляем получение перевода UI
    ui = TEXTS[lang]["ui"]  

    mode = request.form.get("mode", TEXTS[lang]["default_mode"])
    cards = select_cards(TAROT_CARDS)
    interpretation = generate_interpretation(cards, mode, lang)
    spell_message = random.choice(TEXTS[lang]['spell_messages'])
    bun_pool = TEXTS[lang]["bun_messages"].get(mode, TEXTS[lang]["bun_messages"].get("м", []))
    bun_message = random.choice(bun_pool)

    # Дополнительно передаём ui в шаблон
    return render_template(
        "index.html",
        cards=cards,
        interpretation=interpretation,
        spell_message=spell_message,
        bun_message=bun_message,
        mode=mode,
        lang=lang,
        ui=ui   # <-- Эта переменная нужна для локализации текста
    )

if __name__ == "__main__":
    app.run(debug=True)
