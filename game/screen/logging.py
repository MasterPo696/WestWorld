import curses

def display_error(stdscr, message, color_pair):
    """Отображает ошибку на экране."""
    stdscr.addstr(message + "\n", curses.color_pair(color_pair))
    stdscr.refresh()