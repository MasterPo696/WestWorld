
import curses
from game.map.map import print_map
from game.move.movement import move_character

def handle_player_input(stdscr, player_pos, game_map, rows, cols, score, player_stats):
    while True:
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            player_pos, score = move_character("up", player_pos, game_map, rows, cols, score, stdscr, player_stats)
        elif key == curses.KEY_DOWN:
            player_pos, score = move_character("down", player_pos, game_map, rows, cols, score, stdscr, player_stats)
        elif key == curses.KEY_LEFT:
            player_pos, score = move_character("left", player_pos, game_map, rows, cols, score, stdscr, player_stats)
        elif key == curses.KEY_RIGHT:
            player_pos, score = move_character("right", player_pos, game_map, rows, cols, score, stdscr, player_stats)
        elif key == 27:  # ESC key to exit
            break
        
        # Call to print the map after every move
        print_map(stdscr, game_map, score)

    return player_pos, score

