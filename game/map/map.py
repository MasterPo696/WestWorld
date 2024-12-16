import curses
from game.screen.interface import setup_colors
import random
from game.characters.loading import load_master_data
from game.screen.interface import display_equipped_items



        
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
        game_map[fx][fy] = 'T'

    # Размещение стен
    for wx, wy in walls:
        game_map[wx][wy] = '/'

    # Размещение монет
    for cx, cy in coins:
        game_map[cx][cy] = 'C'

    return game_map


def create_maze(rows, cols):
    # Создаем базовую сетку, где все клетки стены
    maze = [['#' for _ in range(cols)] for _ in range(rows)]
    walls = []  # Список для хранения стен
    
    # Функция для прорезания проходов
    def carve_passages(x, y):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Вверх, вниз, влево, вправо
        random.shuffle(directions)  # Перемешиваем направления для случайности
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Новая клетка, куда будет проведен путь
            
            # Проверяем, что клетка находится в пределах карты и является стеной
            if 0 < nx < rows - 1 and 0 < ny < cols - 1 and maze[nx][ny] == '#':  
                maze[nx][ny] = ' '  # Убираем стену
                maze[x + dx // 2][y + dy // 2] = ' '  # Убираем стену между текущей клеткой и новой
                
                carve_passages(nx, ny)  # Рекурсивно прорезаем новые проходы

    # Стартовая точка (необходимо, чтобы она была в центре)
    start_x, start_y = random.randrange(1, rows - 1, 2), random.randrange(1, cols - 1, 2)
    maze[start_x][start_y] = ' '  # Убираем стену с начальной позиции
    carve_passages(start_x, start_y)  # Начинаем процесс создания лабиринта

    # Собираем список стен
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == '#':
                walls.append((i, j))  # Добавляем координаты стены в список

    return walls  # Возвращаем список стен







import random


def generate_position(occupied_positions, rows, cols):
    """Генерация случайных координат для объектов."""
    while True:
        x = random.randint(1, rows - 2)  # Исключаем стены
        y = random.randint(1, cols - 2)
        if (x, y) not in occupied_positions:
            return (x, y)


def create_objects_pos(rows, cols, enemy_count, treasure_count, coins_count):
    # Инициализация списков объектов
    coins = []
    enemies = []
    treasures = []
    # Базовые стены по периметру
    walls = [(0, i) for i in range(cols)] + [(rows - 1, i) for i in range(cols)] + \
            [(i, 0) for i in range(rows)] + [(i, cols - 1) for i in range(rows)]

    # Добавляем растущий коралловый рост стены
    grown_walls = create_maze(rows, cols)

    # Добавляем новые стены из функции grow_walls к общему списку walls
    walls.extend(grown_walls)  # Используем extend, чтобы добавить элементы из grown_walls в walls

    occupied_positions = set(walls)  # Стены уже заняты

    # Генерация позиций для врагов
    for _ in range(enemy_count):
        enemy_pos = generate_position(occupied_positions, rows, cols)
        enemies.append(enemy_pos)
        occupied_positions.add(enemy_pos)

    # Генерация позиций для друзей
    for _ in range(treasure_count):
        treasure_pos = generate_position(occupied_positions, rows, cols)
        treasures.append(treasure_pos)
        occupied_positions.add(treasure_pos)

    # Генерация позиций для монет
    for _ in range(coins_count):
        coin_pos = generate_position(occupied_positions, rows, cols)
        coins.append(coin_pos)
        occupied_positions.add(coin_pos)

    # Позиция игрока
    player_pos = generate_position(occupied_positions, rows, cols)

    return player_pos, enemies, treasures, walls, coins






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
            elif cell == 'T':
                stdscr.addstr(f"{cell} ", curses.color_pair(3))  # Друг - синий
            elif cell == '/':
                stdscr.addstr(f"{cell} ", curses.color_pair(4))  # Стены - голубые
            elif cell == 'C':
                stdscr.addstr(f"{cell} ", curses.color_pair(5))  # Монеты - желтые
            else:
                stdscr.addstr(f"{cell} ")  # Пустое пространство без цвета

        stdscr.addstr("\n")

    y = 1
    x = 55

    character = load_master_data("master")

    stdscr.addstr(y-1, x, f"Персонаж: {character['name']}\n", curses.color_pair(2))  # Счёт - зеленый
    stdscr.addstr(y, x, f"Счёт: {score}\n", curses.color_pair(2))  # Счёт - зеленый

    display_equipped_items(stdscr, character, x, y)
    
    stdscr.refresh()


