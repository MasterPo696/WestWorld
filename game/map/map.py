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

def print_map(stdscr, game_map, score):
    """Отображает карту и текущий счёт на экране."""
    stdscr.clear()
    for row in game_map:
        stdscr.addstr(" ".join(str(cell) for cell in row) + "\n")
    stdscr.addstr(f"Счёт: {score}\n")
    stdscr.refresh()
