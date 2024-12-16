import json
import os 

NPC_PATH = "/Users/masterpo/Desktop/WestWorld/game/characters/npc/"
MASTER_PATH = "/Users/masterpo/Desktop/WestWorld/game/characters/master/"

def save_character_data(character_name, character_data):
    """Сохраняет данные персонажа в JSON файл."""
    file_path = f"{NPC_PATH}{character_name}.json"
    
    # Открываем файл для записи (создаст файл, если его нет)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(character_data, f, ensure_ascii=False, indent=4)


def load_character_data(character_name):
    """Загружает данные персонажа из JSON файла."""
    file_path = os.path.join(NPC_PATH, f"{character_name}.json")
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "name": "Master",
            "params": {
                "intelligence": 5,
                "strength": 6,
                "endurance": 6,
                "courage": 5,
                "perception": 4
            },
            "legend": "Мастер игры",
            "morals": {
                "preserve_nature": "Береги природу и животных.",
                "never_harm": "Не причиняй вреда никому."
            },
            "relations": {},
            "memory": [],
            "mood": 0.5,
            "inventory": {
                "backpack": [],
                "equipped": {
                    "weapon": None,
                    "armor": None,
                    "artifact": None
                },
                "slots": 10
            }
        }
    

def load_master_data(character_name):
    """Загружает данные персонажа из JSON файла."""
    file_path = os.path.join(MASTER_PATH, f"{character_name}.json")
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "name": "Master",
            "params": {
                "intelligence": 5,
                "strength": 6,
                "endurance": 6,
                "courage": 5,
                "perception": 4
            },
            "legend": "Мастер игры",
            "morals": {
                "preserve_nature": "Береги природу и животных.",
                "never_harm": "Не причиняй вреда никому."
            },
            "relations": {},
            "memory": [],
            "mood": 0.5,
            "inventory": {
                "backpack": [],
                "equipped": {
                    "weapon": None,
                    "armor": None,
                    "artifact": None
                },
                "slots": 10
            }
        }