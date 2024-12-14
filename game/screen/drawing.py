import curses
import curses
from config import FACE
import curses

class GameInterface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.character_image = FACE
    
    # Функция для отображения персонажа
    def print_character(self, x, y):
        for i, line in enumerate(self.character_image):
            self.stdscr.addstr(y + i, x, line)

    def print_text(self, text, x, y, max_width):
        # Разбиваем текст на строки, чтобы не выходил за пределы
        words = text.split(' ')  # Разбиваем текст на отдельные слова
        current_line = ""
        lines = []

        for word in words:
            # Если текущее слово не помещается в строку, переносим его на новую строку
            if len(current_line) + len(word) + 1 > max_width:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word

        # Добавляем последнюю строку
        if current_line:
            lines.append(current_line)

        # Выводим каждую строку
        for i, line in enumerate(lines):
            self.stdscr.addstr(y + i, x, line)

    # Функция для рисования интерфейса
    def draw_interface(self, string):
        # Очистка только строки 32, где будет выводиться текст
        self.stdscr.move(32, 0)
        self.stdscr.clrtoeol()

        # Рисуем картинку персонажа
        self.print_character(4, 2)

        # Перемещаем курсор на строку 32 и выводим текст, ограниченный 60 символами
        self.stdscr.move(32, 0)  # Перемещаем курсор на строку 32
        self.print_text(string, 0, 32, 60)  # Максимальная ширина для текста = 60 символов

        self.stdscr.refresh()

# # Основная функция
# def main(stdscr):
#     curses.curs_set(0)
#     interface = GameInterface(stdscr)
#     interface.draw_interface("Это длинный текст, который будет автоматически переноситься на несколько строк. Он должен оставаться внутри рамки и не выходить за пределы экрана.")

#     stdscr.getch()  # Ожидаем нажатия клавиши

# curses.wrapper(main)



def setup_colors():
    """Настраивает цветовые пары для curses."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)   # Красный текст
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Зелёный текст
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Синий текст
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Голубой текст
