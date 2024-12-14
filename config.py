GIGA_API_KEY = "ZWMyNTFkZWEtODBmZS00ODE4LWE4M2YtZmJmN2RhODA4NWNkOmUyZDVmOTlmLTY2MzUtNGY2MS04YjNhLWRhMzJjY2NiODY4NA=="
AI21_API_KEY = "hDAEGAbA9Mg8JWjkJp6GP4G5A5F4du05"

CHAR_DIR = "/Users/masterpo/Desktop/WestWorld/game/characters/npc"

# Params For Characters
TOTAL_POINTS = 20


positive_words = ['друж', 'помо', 'любов', 'добро', 'забота', 'помо', 'друз', 'друг', 'вдох', 'рад', 'положит', 'надеяться']
aggressive_words = ['уби', 'агрессия', 'насилие', 'убий', 'угроза', 'напасть', 'нападение', 'насиловать', 'гнев', 'ненависть', 'зло', 'ударить', 'грубость']
polite_words = ['спасибо', 'пожалуйста', 'извините', 'прощение', 'вежливость', 'извиниться', 'уважать', 'почтение', 'сожаление', 'милость']

positive_words_en = ['friend', 'help', 'love', 'kindness', 'care', 'assistance', 'friends', 'friendliness', 'inspire', 'joy', 'positive', 'hope']
aggressive_words_en = ['kill', 'aggression', 'violence', 'murder', 'threat', 'attack', 'assault', 'rape', 'anger', 'hate', 'evil', 'hit', 'rudeness']
polite_words_en = ['thank you', 'please', 'sorry', 'apology', 'politeness', 'excuse me', 'respect', 'regard', 'regret', 'mercy']

POSITIVE = [positive_words, positive_words_en]
AGGRESSIVE = [aggressive_words, aggressive_words_en]
POLITE = [polite_words, polite_words_en]



PARAM_NAMES = [
    "intelligence", "strength", "endurance", 
    "courage", "perception"
]

FACE = [
            "        ########################",
            "      ##                        ##",
            "    ##                            ##",
            "   ##    O                   O    ##",
            "  ##                                ##",
            " ##                                 ##",
            " ##    ####                ####     ##",
            " ##   #    #              #    #    ##",
            " ##   #    #              #    #    ##",
            " ##   #    #    ___       #    #    ##",
            "  ##   ####    /    \\     ####    ##",
            "   ##          |     |           ##",
            "    ##         |     |          ##",
            "     ##        |_____|         ##",
            "      ##                      ##",
            "       ########################"
        ]

MORAL_POOL = [
            {"key": "help_others", "description": "Помогай другим в беде."},
            {"key": "never_harm", "description": "Не причиняй вреда никому."},
            {"key": "value_freedom", "description": "Свобода превыше всего."},
            {"key": "seek_knowledge", "description": "Постоянно стремись к новым знаниям."},
            {"key": "protect_weak", "description": "Защищай слабых."},
            {"key": "honor_loyalty", "description": "Цени верность выше всего."},
            {"key": "revenge_wrongs", "description": "Всегда мсти за несправедливость."},
            {"key": "preserve_nature", "description": "Береги природу и животных."},
            {"key": "embrace_chaos", "description": "Следуй за хаосом, не люби порядок."},
            {"key": "pursue_power", "description": "Добивайся силы и влияния любой ценой."}
        ]

# Статы игрока
PLAYER_STATS = {
    "intelligence": 5,
    "strength": 6,
    "endurance": 6,
    "courage": 5,
    "perception": 4
}