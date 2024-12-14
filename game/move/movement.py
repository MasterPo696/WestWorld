from game.actions.interaction import interact_with_character

import os 
from config import CHAR_DIR
import random
import logging
import json

def characters_list():
    char_list = os.listdir(CHAR_DIR)
    return char_list

def move_character(direction, player_pos, game_map, rows, cols, score, stdscr, player_stats):
    """Двигает персонажа в указанном направлении, обновляя карту, счёт и взаимодействие."""

    
    # stdscr.addstr(f"{stdscr, False, player_stats, score}")
    # return
    
    x, y = player_pos
    game_map[x][y] = " "  # Очищаем старую позицию
    new_x, new_y = x, y

    if direction == "up" and x > 0:
        new_x -= 1
    elif direction == "down" and x < rows - 1:
        new_x += 1
    elif direction == "left" and y > 0:
        new_y -= 1
    elif direction == "right" and y < cols - 1:
        new_y += 1

    # Проверка на стены
    if game_map[new_x][new_y] == '/':
        return player_pos, score

    # Проверка на врагов
    if game_map[new_x][new_y] == 'V':
        # char_list = characters_list()  # Пример имени врага
        enemy_name = "Arthas"
        # enemy_name = char_list[random.randrange(0, len(char_list))]

        defeated, score = interact_with_character(stdscr, enemy_name, False, player_stats, score)
        if defeated:
            game_map[new_x][new_y] = " "
        else:
            return player_pos, score
        
        # Проверка на монеты
    if game_map[new_x][new_y] == 'C':
        score += 1

    # Проверка на друзей
    if game_map[new_x][new_y] == 'F':
        friend_name = "Ally"  # Пример имени друга
        interact_with_character(stdscr, friend_name, True, player_stats, score)

    # Обновляем позицию игрока
    player_pos = (new_x, new_y)
    game_map[player_pos[0]][player_pos[1]] = 'X'
    return player_pos, score
