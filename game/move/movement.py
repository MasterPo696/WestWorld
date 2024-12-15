from game.actions.interaction import interact_with_character
from game.characters.creation import CreateCharacter
import os 
import curses
from config import CHAR_DIR
import random
import logging
import json

def load_character_data2(name):
    """Загружает данные персонажа из файла."""
    # Пример данных персонажа, для теста
    return {
        'name': name,
        'legend': 'Старый рыцарь, который искал славу.',
        'params': {'endurance': 100, 'strength': 50, 'intelligence': 30},
        'morals': 'Добрые',
        'mood': 'Счастлив',
        'relations': {'master': 0.7}
    }


# Функция для управления движением персонажа
def move_character(direction, player_pos, game_map, rows, cols, score, stdscr, player_stats):
    """Двигает персонажа в указанном направлении, обновляя карту, счёт и взаимодействие."""

    x, y = player_pos
    game_map[x][y] = " "  # Очищаем старую позицию
    new_x, new_y = x, y

    # Двигаем персонажа в соответствующем направлении
    if direction == "up" and x > 0:
        new_x -= 1
    elif direction == "down" and x < rows - 1:
        new_x += 1
    elif direction == "left" and y > 0:
        new_y -= 1
    elif direction == "right" and y < cols - 1:
        new_y += 1

    # Проверка на столкновение со стеной
    if game_map[new_x][new_y] == '/':
        game_map[x][y] = 'X'  # Возвращаем персонажа на исходную позицию
        return player_pos, score  # Персонаж не двигается

    # Проверка на врагов
    if game_map[new_x][new_y] == 'V':
        enemy_name = "Arthas"
        defeated, score = interact_with_character(stdscr, enemy_name, False, player_stats, score, rows)
        if defeated:
            game_map[new_x][new_y] = " "  # Убираем врага, если побежден
        else:
            return player_pos, score  # Если не побежден, не двигаем игрока

    # Проверка на монеты
    if game_map[new_x][new_y] == 'C':
        score += 1  # Увеличиваем счет, если монета

    # Проверка на друзей
    if game_map[new_x][new_y] == 'F':
        friend_name = "Ally"  # Пример имени друга
        interact_with_character(stdscr, friend_name, True, player_stats, score, rows)

    # Обновляем позицию игрока
    player_pos = (new_x, new_y)
    game_map[player_pos[0]][player_pos[1]] = 'X'  # Перемещаем персонажа на новую позицию
    return player_pos, score
