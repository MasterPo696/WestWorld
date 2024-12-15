import curses
import curses
from config import FACE
import curses

class GameInterface:
    def __init__(self, stdscr, rows):
        self.stdscr = stdscr
        self.character_image = FACE
        self.rows = rows
    
    # Функция для отображения персонажа
    def print_character(self, x, y):
        for i, line in enumerate(self.character_image):
            self.stdscr.addstr(y + i+5, x, line)

    def print_text(self, text, x, y):
        """Просто выводит текст без переноса строк."""
        self.stdscr.addstr(y, x, text)  # Выводим текст на заданной позиции
        self.stdscr.refresh()

    # Функция для рисования интерфейса
    def draw_interface(self, string, character_data):
        height, width = self.stdscr.getmaxyx()

        # Разделим экран на 3 части: слева (для лица), справа (для статистики), снизу (для текста)
        face_width = 110  # Ширина для лица персонажа
        stats_width = width - face_width  # Оставшееся место для статистики

        # Очистим окна
        self.stdscr.clear()

        # Отображаем лицо персонажа слева
        self.print_character(2, 2)

        x = 11
        # Отображаем статистику справа
        self.stdscr.addstr(2 + x, stats_width, f"Имя: {character_data['name']}", curses.color_pair(2))
        self.stdscr.addstr(3 + x, stats_width, f"Здоровье: {character_data['params']['endurance']}", curses.color_pair(2))
        self.stdscr.addstr(4 + x, stats_width, f"Сила: {character_data['params']['strength']}", curses.color_pair(2))
        self.stdscr.addstr(5 + x, stats_width, f"Интеллект: {character_data['params']['intelligence']}", curses.color_pair(2))

        # Нижняя строка для текста
        self.stdscr.addstr(height - 16, 0, string, curses.color_pair(1))

        self.stdscr.refresh()

def setup_colors():
    """Настраивает цветовые пары для curses."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)   # Красный текст
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Зелёный текст
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Синий текст
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Голубой текст
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Желтый текст

    