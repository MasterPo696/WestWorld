import curses

def setup_colors():
    """Настраивает цветовые пары для curses."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)   # Красный текст
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Зелёный текст
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Синий текст
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Голубой текст
