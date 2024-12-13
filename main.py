import curses
import random
from game.map.map import create_map, print_map
from game.move.movement import move_character
from game.move.keyboard import handle_player_input
from game.characters.functions.creation import CreateCharacter
from game.map.position import create_objects_pos

# Статы игрока
PLAYER_STATS = {
            "intelligence": 5,
            "strength": 6,
            "cunning": 7,
            "kindness": 4,
            "charisma": 5,
            "endurance": 6,
            "perception": 4,
            "creativity": 3,
            "courage": 5,
            "empathy": 4
        }

import random

def main(stdscr):
    try:
        curses.curs_set(0)

        player_stats = PLAYER_STATS

        rows, cols = 10, 10
        score = 0

        player_pos, enemies_pos, friends_pos, walls, coins = create_objects_pos(rows, cols, enemy_count=2, fren_count=3, coins_count=4)
        
        # character_creator = CreateCharacter()
        
        game_map = create_map(rows, cols, player_pos, enemies_pos, friends_pos, walls, coins)
        print_map(stdscr, game_map, score=0)
        
        player_pos, score = handle_player_input(stdscr, player_pos, game_map, rows, cols, score, player_stats)

    except KeyboardInterrupt:
        stdscr.clear()
        stdscr.addstr("Игра прервана нажатием команды.\n")
        stdscr.refresh()
        curses.napms(2000)
    finally:
        curses.endwin()

curses.wrapper(main)