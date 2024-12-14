import json
def load_character_data(name):
    """Загружает данные персонажа из файла."""
    with open(f'game/characters/npc/{name}.json', 'r') as file:
        return json.load(file)

