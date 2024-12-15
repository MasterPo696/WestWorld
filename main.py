import curses
import random
from game.map.map import create_map, print_map
from game.move.movement import move_character
from game.move.keyboard import handle_player_input
from game.characters.creation import CreateCharacter, CreateUser
from game.map.map import create_objects_pos
from config import PLAYER_STATS
from game.screen.interface import setup_colors

def main(stdscr):
    try:
        curses.curs_set(0)

        player_stats = PLAYER_STATS
        rows, cols = 25, 25
        score = 0

        cc, fc, ec = rows//2, rows//3, rows//4
        # Настройка цветов
        setup_colors()  # Теперь эта строка не закомментирована
        # Генерация объектов на карте
        pp, ep, fp, wp, cp = create_objects_pos(rows, cols, int(ec), int(fc), int(cc))
        game_map = create_map(rows, cols, pp, ep, fp, wp, cp)
        print_map(stdscr, game_map, score=0)

        # Обработка ввода игрока и обновление карты
        pp, score = handle_player_input(stdscr, pp, game_map, rows, cols, score, player_stats)

    except KeyboardInterrupt:
        stdscr.clear()
        stdscr.addstr("Игра прервана нажатием команды.\n")
        stdscr.refresh()
        curses.napms(2000)
    finally:
        curses.endwin()

curses.wrapper(main)
