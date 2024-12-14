import json
import os 

PATH = "/Users/masterpo/Desktop/WestWorld/game/characters/npc/"

def save_character_data(character_name, character_data):
    """Сохраняет данные персонажа в JSON файл."""
    file_path = f"{PATH}{character_name}.json"
    
    # Открываем файл для записи (создаст файл, если его нет)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(character_data, f, ensure_ascii=False, indent=4)

def load_character_data(character_name):
    """Загружает данные персонажа из JSON файла."""
    file_path = f"{character_name}.json"
    
    if os.path.exists(file_path):
        # Если файл существует, загружаем данные
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Если файла нет, возвращаем пустой шаблон
        return {
            "name": character_name,
            "params": {
                "intelligence": 5,
                "strength": 6,
                "endurance": 6,
                "courage": 5,
                "perception": 4
            },
            "legend": "Старый паренек, искал удачи в поиске сокровищ, любит придумывать истории и восхвалять себя",
            "morals": {
                "preserve_nature": "Береги природу и животных.",
                "never_harm": "Не причиняй вреда никому."
            },
            "relations": {},
            "memory": [],
            "mood": 0.5
        }

