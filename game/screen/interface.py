import curses
import curses
from config import FACE
import curses

def print_slowly(stdscr, string, height, width):
        """Печатает строку по одному символу с задержкой 0.15 секунд."""
        for i in range(len(string)):
            # Выводим символ
            stdscr.addstr(height - 16, width, string[:i+1], curses.color_pair(1))
            stdscr.refresh()
            time.sleep(0.05)  # Задержка перед выводом следующего символа

        stdscr.refresh()

class GameInterface:
    def __init__(self, stdscr, rows):
        self.stdscr = stdscr
        self.character_image = FACE
        self.rows = rows
    
    # Функция для отображения персонажа
    def print_character(self, x, y):
        for i, line in enumerate(self.character_image):
            self.stdscr.addstr(y + i + 5, x, line)

    def print_text(self, text, x, y):
        """Просто выводит текст без переноса строк."""
        self.stdscr.addstr(y, x, text)  # Выводим текст на заданной позиции
        self.stdscr.refresh()

    


    # Функция для рисования интерфейса
    def draw_interface(self, string, character_data):
        height, width = self.stdscr.getmaxyx()

        # Разделим экран на 3 части: слева (для лица), справа (для статистики), снизу (для текста)
        face_width = 68  # Ширина для лица персонажа
        stats_width = width - face_width  # Оставшееся место для статистики


        y = 11
        # Отображаем лицо персонажа слева
        self.print_character(50, 2)
        

        
        # Отображаем статистику справа
        self.stdscr.addstr(2 + y, stats_width, f"Имя: {character_data['name']}", curses.color_pair(2))
        self.stdscr.addstr(3 + y, stats_width, f"Здоровье: {character_data['params']['endurance']}", curses.color_pair(2))
        self.stdscr.addstr(4 + y, stats_width, f"Сила: {character_data['params']['strength']}", curses.color_pair(2))
        self.stdscr.addstr(5 + y, stats_width, f"Интеллект: {character_data['params']['intelligence']}", curses.color_pair(2))

        # Нижняя строка для текста
        print_slowly(self.stdscr, string, height, 0)
        # self.stdscr.addstr(height - 16, 0, string, curses.color_pair(1))

        self.stdscr.refresh()

def setup_colors():
    """Настраивает цветовые пары для curses."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)   # Красный текст
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Зелёный текст
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Синий текст
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Голубой текст
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Желтый текст


import curses
import time



def display_equipped_items(stdscr, character, x, y):
    """Отображает экипированные предметы с их параметрами улучшений."""
    
    # Получаем информацию о экипированных предметах
    weapon_name = character['inventory']['equipped']['weapon']['name'] if character['inventory']['equipped']['weapon'] else "Пусто"
    armor_name = character['inventory']['equipped']['armor']['name'] if character['inventory']['equipped']['armor'] else "Пусто"
    artifact_name = character['inventory']['equipped']['artifact']['name'] if character['inventory']['equipped']['artifact'] else "Пусто"
    
    # Получаем параметры, которые улучшают предметы
    weapon_effects = character['inventory']['equipped']['weapon'].get('effect', {}) if character['inventory']['equipped']['weapon'] else {}
    armor_effects = character['inventory']['equipped']['armor'].get('effect', {}) if character['inventory']['equipped']['armor'] else {}
    artifact_effects = character['inventory']['equipped']['artifact'].get('effect', {}) if character['inventory']['equipped']['artifact'] else {}

    # Формируем строки для отображения параметров улучшений
    weapon_effect_str = ", ".join([f"{key}: {value}" for key, value in weapon_effects.items()]) if weapon_effects else "Пусто"
    armor_effect_str = ", ".join([f"{key}: {value}" for key, value in armor_effects.items()]) if armor_effects else "Пусто"
    artifact_effect_str = ", ".join([f"{key}: {value}" for key, value in artifact_effects.items()]) if artifact_effects else "Пусто"

    # Отображаем название предмета и его параметры
    stdscr.addstr(y + 1, x, f"Оружие: {weapon_name} ({weapon_effect_str})")
    stdscr.addstr(y + 2, x, f"Броня: {armor_name} ({armor_effect_str})")
    stdscr.addstr(y + 3, x, f"Артефакт: {artifact_name} ({artifact_effect_str})")
    
    stdscr.refresh()

