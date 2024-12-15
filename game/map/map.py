import curses
from game.screen.interface import setup_colors
import random



        
# Функция для создания карты
def create_map(rows, cols, player_pos, enemies, friends, walls, coins):
    """
    Создает игровую карту.

    :param rows: Количество строк карты
    :param cols: Количество столбцов карты
    :param player_pos: Координаты игрока (строка, столбец)
    :param enemies: Список координат врагов [(строка, столбец), ...]
    :param friends: Список координат друзей [(строка, столбец), ...]
    :param walls: Список координат стен [(строка, столбец), ...]
    :param coins: Список координат монет [(строка, столбец), ...]
    :return: Двумерный массив, представляющий карту
    """
    game_map = [[" " for _ in range(cols)] for _ in range(rows)]

    # Размещение игрока
    x, y = player_pos
    game_map[x][y] = 'X'

    # Размещение врагов
    for ex, ey in enemies:
        game_map[ex][ey] = 'V'

    # Размещение друзей
    for fx, fy in friends:
        game_map[fx][fy] = 'F'

    # Размещение стен
    for wx, wy in walls:
        game_map[wx][wy] = '/'

    # Размещение монет
    for cx, cy in coins:
        game_map[cx][cy] = 'C'

    return game_map

# def print_map(stdscr, game_map, score):
#     """Отображает карту и текущий счёт на экране."""
#     stdscr.clear()
#     for row in game_map:
#         stdscr.addstr(" ".join(str(cell) for cell in row) + "\n")
#     stdscr.addstr(f"Счёт: {score}\n")
#     stdscr.refresh()

import random

def grow_walls(rows, cols, start_x, start_y, growth_limit=20):
    """Функция для кораллового роста стен, начиная с случайной точки на верхней стене."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо
    walls = set([(start_x, start_y)])  # Начальная точка
    occupied_positions = set(walls)  # Стены уже заняты

    growth_count = 0
    while growth_count < growth_limit:
        # Случайным образом выбираем одну из стен для роста
        x, y = random.choice(list(walls))
        random.shuffle(directions)  # Перемешиваем направления для случайности

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            # Проверяем, что новая позиция внутри карты и не занята
            if 1 <= new_x < rows - 1 and 1 <= new_y < cols - 1 and (new_x, new_y) not in occupied_positions:
                walls.add((new_x, new_y))
                occupied_positions.add((new_x, new_y))
                growth_count += 1
                break

    return list(walls)


def generate_position(occupied_positions, rows, cols):
    """Генерация случайных координат для объектов."""
    while True:
        x = random.randint(1, rows - 2)  # Исключаем стены
        y = random.randint(1, cols - 2)
        if (x, y) not in occupied_positions:
            return (x, y)

def create_objects_pos(rows, cols, enemy_count, friend_count, coins_count):
    # Инициализация списков объектов
    coins = []
    enemies_pos = []
    friends_pos = []
    # Базовые стены по периметру
    walls = [(0, i) for i in range(cols)] + [(rows - 1, i) for i in range(cols)] + \
            [(i, 0) for i in range(rows)] + [(i, cols - 1) for i in range(rows)]

    # Случайная точка на верхней стене для начала роста
    start_x, start_y = 0, random.randint(1, cols - 2)  # Выбираем случайную точку на верхней стене

    # Добавляем растущий коралловый рост стены
    grown_walls = grow_walls(rows, cols, start_x, start_y, growth_limit=20)

    # Добавляем новые стены из функции grow_walls к общему списку walls
    walls.extend(grown_walls)  # Используем extend, чтобы добавить элементы из grown_walls в walls

    occupied_positions = set(walls)  # Стены уже заняты



    # Генерация позиций для врагов
    for _ in range(enemy_count):
        enemy_pos = generate_position(occupied_positions, rows, cols)
        enemies_pos.append(enemy_pos)
        occupied_positions.add(enemy_pos)

    # Генерация позиций для друзей
    for _ in range(friend_count):
        friend_pos = generate_position(occupied_positions, rows, cols)
        friends_pos.append(friend_pos)
        occupied_positions.add(friend_pos)

    # Генерация позиций для монет
    for _ in range(coins_count):
        coin_pos = generate_position(occupied_positions, rows, cols)
        coins.append(coin_pos)
        occupied_positions.add(coin_pos)

    # Позиция игрока
    player_pos = generate_position(occupied_positions, rows, cols)

    return player_pos, enemies_pos, friends_pos, walls, coins



def print_map(stdscr, game_map, score):
    """Отображает карту и текущий счёт на экране с цветами."""
    stdscr.clear()

    setup_colors()
    for row in game_map:
        for cell in row:
            if cell == 'X':
                stdscr.addstr(f"{cell} ", curses.color_pair(2))  # Игрок - зеленый
            elif cell == 'V':
                stdscr.addstr(f"{cell} ", curses.color_pair(1))  # Враг - красный
            elif cell == 'F':
                stdscr.addstr(f"{cell} ", curses.color_pair(3))  # Друг - синий
            elif cell == '/':
                stdscr.addstr(f"{cell} ", curses.color_pair(4))  # Стены - голубые
            elif cell == 'C':
                stdscr.addstr(f"{cell} ", curses.color_pair(5))  # Монеты - желтые
            else:
                stdscr.addstr(f"{cell} ")  # Пустое пространство без цвета

        stdscr.addstr("\n")

    stdscr.addstr(f"Счёт: {score}\n", curses.color_pair(2))  # Счёт - зеленый
    stdscr.refresh()
