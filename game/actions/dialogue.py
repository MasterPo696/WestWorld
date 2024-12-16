from game.characters.loading import load_character_data, save_character_data
import curses
from config import POSITIVE, AGGRESSIVE, POLITE

def get_user_input(stdscr, rows):
    """Получает пользовательский ввод с обработкой команд и Ctrl+S."""
    # Устанавливаем курсор на строку ввода
    stdscr.move(rows+6, 2)
    stdscr.addstr("\nВаше сообщение (CNTRL C для завершения): ", curses.color_pair(3))
    stdscr.refresh()
    
    # Включаем режим ввода текста
    curses.echo()
    
    # Получаем строку ввода
    user_input = stdscr.getstr().decode('utf-8', errors='ignore').strip()
    
    # Отключаем режим ввода текста
    curses.noecho()

    # Очищаем строку ввода, перемещая курсор в начало строки и очищая её
    stdscr.move(rows+6, 2)
    stdscr.clrtoeol()  # Очищаем строку после ввода

    return user_input

def evaluate_dialogue(user_input, character_data):
    """
    Оценка поведения игрока (мастера) в диалоге.
    Поведение оценивается от 0 (плохое) до 1 (хорошее).
    """
    # Получаем текущее значение отношения из relations
    current_score = character_data['relations'].get('master', 0.5)

    # Начальная оценка
    score = current_score

    # Оценка на основе ввода пользователя
    for word_list in [POSITIVE, AGGRESSIVE, POLITE]:
        for word in word_list[0] + word_list[1]:  # Объединяем список слов для обоих языков
            if word in user_input.lower():  # Приводим к нижнему регистру для поиска
                if word in POSITIVE[0] or word in POSITIVE[1]:
                    score += 0.2  # Доброе поведение
                elif word in AGGRESSIVE[0] or word in AGGRESSIVE[1]:
                    score -= 0.3  # Агрессия или угроза
                elif word in POLITE[0] or word in POLITE[1]:
                    score += 0.1  # Вежливость

    # Ограничиваем оценку, чтобы она была в пределах [0, 1]
    score = max(0, min(score, 1))

    # Обновляем отношение в relations
    character_data['relations']['master'] = score

    # Сохраняем обновленные данные в файл
    save_character_data(character_data['name'], character_data)

    return score

def generate_npc_response(ai21, sys_msg, conversation_history):
    """Генерирует ответ NPC с использованием AI21."""
    response = ai21.generate_response(sys_msg, "\n".join(conversation_history))
    if not response:
        return None
    return response
