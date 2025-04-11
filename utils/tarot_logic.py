import random
from openai import OpenAI

# 🔮 Полная колода карт
TAROT_CARDS = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune",
    "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower",
    "The Star", "The Moon", "The Sun", "Judgement", "The World",
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands",
    "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands",
    "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands",
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups",
    "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups",
    "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords",
    "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords",
    "Page of Swords", "Knight of Swords", "Queen of Swords", "King of Swords",
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles",
    "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles",
    "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles"
]

def select_cards(card_list=TAROT_CARDS, count=3):
    selected = random.sample(card_list, count)
    result = []
    for card in selected:
        reversed_card = random.random() < 0.3
        filename = card.lower().replace(" ", "_") + ".jpg"
        result.append({"name": card, "reversed": reversed_card, "filename": filename})
    return result

def generate_interpretation(cards, mode):
    mode_text = {
        "ж": "любовный расклад",
        "м": "общий расклад",
        "совет": "расклад на совет",
        "дух": "расклад на внутренний рост",
        "кризис": "расклад на сложную ситуацию"
    }.get(mode, "расклад")

    description = "\n".join([
        f"{card['name']} (перевёрнута)" if card['reversed'] else f"{card['name']}"
        for card in cards
    ])

    prompt = (
        "Ты - близкая волшебная подруга, которая делает " + mode_text + ".\n"
        "Вот карты: " + description + "\n"
        "Объясни расклад доброжелательно, с юмором, без использования пола, без 'дорогая' и 'друг'. "
        "Можно обращаться 'солнышко', 'заечка', 'звёздочка', 'булочка' и подобные нейтральные ласковые слова. "
        "Не используй 'вы' или 'обращайтесь за помощью'. Напиши, как будто рассказываешь подруге или другу лично."
    )

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты - добрая волшебная подруга, которая гадает на Таро. Рассказывай нежно, с юмором и с любовью. Говори на ты, но избегай гендерных обращений."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    return response.choices[0].message.content

def get_random_bun_message():
    messages = [
        "🔮 Сегодня звезды на твоей стороне. Доверься интуиции!",
        "✨ Даже булочка знает: впереди волшебные перемены.",
        "🌠 Ты сильнее, чем кажется — магия уже внутри тебя.",
        "🌌 Оглянись — мир полон чудес, и одно из них направляется к тебе.",
        "🪄 Пусть этот день принесет тебе вдохновение и уверенность."
    ]
    return random.choice(messages)

__all__ = ['TAROT_CARDS', 'select_cards', 'generate_interpretation', 'get_random_bun_message']