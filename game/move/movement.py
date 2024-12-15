from game.actions.interaction import interact_with_character
from game.characters.creation import CreateCharacter
import os 
import curses
from config import CHAR_DIR
import random
import logging
import json



# Функция для управления движением персонажа
def move_character(direction, player_pos, game_map, rows, cols, score, stdscr, player_stats):
    """Двигает персонажа в указанном направлении, обновляя карту, счёт и взаимодействие."""

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

    # Проверка на стены
    if game_map[new_x][new_y] == '/':
        return player_pos, score

    # Проверка на врагов
    if game_map[new_x][new_y] == 'V':
        # create_character_if_not_exist(stdscr, score, character_name, characters)
        # char_list = characters_list()  # Пример имени врага
        enemy_name = "Arthas"
        # name = char_list[random.randrange(0, len(char_list))]

        defeated, score = interact_with_character(stdscr, enemy_name, False, player_stats, score, rows)
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
        interact_with_character(stdscr, friend_name, True, player_stats, score, rows)

    # Обновляем позицию игрока
    player_pos = (new_x, new_y)
    game_map[player_pos[0]][player_pos[1]] = 'X'
    return player_pos, score
