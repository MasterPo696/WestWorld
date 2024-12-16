# import os
# import json
# import random
from game.characters.loading import load_master_data
ITEMS_DIR = "/Users/masterpo/Desktop/WestWorld/game/characters/items/"

# def load_items():
#     """Загружает все предметы из JSON файлов в указанной директории."""
#     items = []
#     for filename in os.listdir(ITEMS_DIR):
#         if filename.endswith(".json"):  # Обрабатываем только JSON файлы
#             filepath = os.path.join(ITEMS_DIR, filename)
#             with open(filepath, 'r', encoding='utf-8') as file:
#                 data = json.load(file)
#                 items.extend(data)  # Добавляем предметы в общий список
#     return items

# def generate_treasure_item():

#     items = load_items()
#     """Генерирует случайный предмет из списка с учетом вероятности."""
#     # Определим вероятности выпадения предметов разных типов
#     # Более сильные предметы будут выпадать реже
#     common_items = [item for item in items if item["rarity"] == "common"]
#     rare_items = [item for item in items if item["rarity"] == "rare"]
#     epic_items = [item for item in items if item["rarity"] == "epic"]
#     legendary_items = [item for item in items if item["rarity"] == "legendary"]

#     # Логика для выпадения предметов с разной вероятностью
#     rarity_roll = random.random()

#     if rarity_roll < 0.6:
#         # 60% шанс на обычный предмет
#         return random.choice(common_items)
#     elif rarity_roll < 0.85:
#         # 25% шанс на редкий предмет
#         return random.choice(rare_items)
#     elif rarity_roll < 0.95:
#         # 10% шанс на эпический предмет
#         return random.choice(epic_items)
#     else:
#         # 5% шанс на легендарный предмет
#         return random.choice(legendary_items)

# def interact_with_treasure(stdscr, score):
#     """Механика взаимодействия с сокровищем."""
    
#     # Генерация случайного объекта
#     item = generate_treasure_item()
    
#     # Показываем описание объекта
#     description = item["description"]
#     stdscr.clear()
#     stdscr.addstr(2, 0, f"Вы нашли {item['name']}!")
#     stdscr.addstr(3, 0, f"Описание: {description}")
#     stdscr.addstr(5, 0, f"Хотите взять? (y/n)")

#     stdscr.refresh()
#     character = load_character_data("master")
#     inventory = character.get('inventory')

#     # Ожидаем ввода игрока
#     key = stdscr.getch()
    
#     # Если игрок нажимает 'y', добавляем объект в инвентарь
#     if key == ord('y'):
#         inventory.append(item)
#         stdscr.addstr(7, 0, f"Вы добавили {item['name']} в инвентарь.")
#     elif key == ord('n'):
#         stdscr.addstr(7, 0, "Вы отказались от предмета.")
    
#     stdscr.refresh()
#     stdscr.getch()  # Ожидаем следующего ввода, чтобы игрок мог увидеть результат

#     return inventory, score


# # # Пример использования
# # items = load_items()  # Загружаем все предметы
# # treasure_item = generate_treasure_item(items)  # Генерируем случайный предмет

# # print(f"Вы нашли предмет: {treasure_item['name']}")


import os
import json
import random

ITEMS_DIR = "/Users/masterpo/Desktop/WestWorld/game/characters/items/"
PATH = "/Users/masterpo/Desktop/WestWorld/game/characters/master/"

def load_items():
    """Загружает все предметы из JSON файлов в указанной директории."""
    items = []
    for filename in os.listdir(ITEMS_DIR):
        if filename.endswith(".json"):  # Обрабатываем только JSON файлы
            filepath = os.path.join(ITEMS_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                items.extend(data)  # Добавляем предметы в общий список
    return items

def generate_treasure_item():
    """Генерирует случайный предмет из списка с учетом вероятности."""
    items = load_items()
    
    # Определим вероятности выпадения предметов разных типов
    common_items = [item for item in items if item["rarity"] == "common"]
    rare_items = [item for item in items if item["rarity"] == "rare"]
    epic_items = [item for item in items if item["rarity"] == "epic"]
    legendary_items = [item for item in items if item["rarity"] == "legendary"]

    rarity_roll = random.random()

    if rarity_roll < 0.6:
        # 60% шанс на обычный предмет
        return random.choice(common_items)
    elif rarity_roll < 0.85:
        # 25% шанс на редкий предмет
        return random.choice(rare_items)
    elif rarity_roll < 0.95:
        # 10% шанс на эпический предмет
        return random.choice(epic_items)
    else:
        # 5% шанс на легендарный предмет
        return random.choice(legendary_items)


def save_character_data(character_name, character_data):
    """Сохраняет данные персонажа в JSON файл."""
    file_path = os.path.join(PATH, f"{character_name}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(character_data, f, ensure_ascii=False, indent=4)

def interact_with_treasure(stdscr, score):
    """Механика взаимодействия с сокровищем."""
    
    # Генерация случайного объекта
    item = generate_treasure_item()

    x = 55
    # Показываем описание объекта
    description = item["description"]
    stdscr.addstr(7, x, f"Вы нашли {item['name']}!")
    stdscr.addstr(8, x, f"Описание: {description}")
    stdscr.addstr(9, x, f"Хотите взять? (y/n)")

    stdscr.refresh()
    character = load_master_data("master")
    inventory = character.get('inventory')

    

    # Ожидаем ввода игрока
    key = stdscr.getch()
    
    # Если игрок нажимает 'y', добавляем объект в инвентарь
    if key == ord('y'):
        item_type = item.get('type')

        # Проверяем, есть ли уже предмет этого типа в экипировке
        if item_type == "weapon" and character["inventory"]["equipped"]["weapon"] is None:
            character["inventory"]["equipped"]["weapon"] = item
            stdscr.addstr(10, x, f"Вы экипировали {item['name']} как оружие.")
        elif item_type == "armor" and character["inventory"]["equipped"]["armor"] is None:
            character["inventory"]["equipped"]["armor"] = item
            stdscr.addstr(10, x, f"Вы экипировали {item['name']} как броню.")
        elif item_type == "artifact" and character["inventory"]["equipped"]["artifact"] is None:
            character["inventory"]["equipped"]["artifact"] = item
            stdscr.addstr(10, x, f"Вы экипировали {item['name']} как артефакт.")
        else:
            # Проверяем, есть ли место в рюкзаке
            if len(inventory["backpack"]) < inventory["slots"]:
                # Добавляем предмет в рюкзак
                inventory["backpack"].append(item)
                stdscr.addstr(7, x, f"Вы добавили {item['name']} в рюкзак.")
            else:
                stdscr.addstr(7, x, "Ваш рюкзак полон!")

        save_character_data("master", character)  # Сохраняем изменения

    elif key == ord('n'):
        stdscr.addstr(7, 0, "Вы отказались от предмета.")
    
    stdscr.refresh()
    stdscr.getch()  # Ожидаем следующего ввода, чтобы игрок мог увидеть результат

    return inventory, score
