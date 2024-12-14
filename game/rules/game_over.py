import curses
# Остальные функции (create_map, print_map) остаются здесь.

def game_over(stdscr, score):
    """Обрабатывает окончание игры."""
    stdscr.clear()
    stdscr.addstr("Вы погибли! Игра окончена.\n")
    stdscr.addstr(f"Ваш итоговый счёт: {score}\n")
    stdscr.refresh()
    curses.napms(2000)
    raise SystemExit


