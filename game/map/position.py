import random

def create_objects_pos(rows, cols, enemy_count, fren_count, coins_count):
    # Функция для генерации случайных координат, не пересекающихся с другими объектами
    def generate_position(occupied_positions):
        while True:
            x = random.randint(1, rows - 2)  # Исключаем стенки
            y = random.randint(1, cols - 2)
            if (x, y) not in occupied_positions:
                return (x, y)

    # Начальные координаты объектов
    coins = []
    enemies_pos = []
    friends_pos = []
    walls = [(0, i) for i in range(cols)] + [(rows - 1, i) for i in range(cols)] + \
            [(i, 0) for i in range(rows)] + [(i, cols - 1) for i in range(rows)]

    occupied_positions = set(walls)  # Стены уже заняты

    # Генерация позиций для врагов
    for _ in range(enemy_count):
        enemy_pos = generate_position(occupied_positions)
        enemies_pos.append(enemy_pos)
        occupied_positions.add(enemy_pos)

    # Генерация позиций для друзей
    for _ in range(fren_count):
        friend_pos = generate_position(occupied_positions)
        friends_pos.append(friend_pos)
        occupied_positions.add(friend_pos)

    # Генерация позиций для монет
    for _ in range(coins_count):
        coin_pos = generate_position(occupied_positions)
        coins.append(coin_pos)
        occupied_positions.add(coin_pos)

    # Позиция игрока
    player_pos = generate_position(occupied_positions)

    return player_pos, enemies_pos, friends_pos, walls, coins