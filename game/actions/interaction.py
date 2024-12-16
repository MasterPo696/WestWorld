import random
import curses
import json

from game.llm.ai21 import LLMServiceAI21
from game.screen.interface import setup_colors
from game.actions.battle import start_battle
from game.rules.game_over import game_over
from game.characters.loading import load_character_data, save_character_data
from game.screen.logging import display_error
from game.screen.interface import GameInterface
from game.actions.dialogue import generate_npc_response, evaluate_dialogue, get_user_input
import curses
from config import FACE



def get_input():
    user_input = input().strip()  # Получаем строку от пользователя и убираем лишние пробелы
    return user_input


from config import FACE


def interact_with_character(stdscr, character_name, is_friend, player_stats, score, rows):
    """Основная функция для взаимодействия с персонажем."""
    ai21 = LLMServiceAI21()  # Инициализация AI21 сервиса
    setup_colors()  # Настройка цветов для curses

    try:
        # Загружаем данные персонажа
        character_data = load_character_data(character_name)
    except FileNotFoundError:
        display_error(stdscr, "[Ошибка: Не удалось загрузить данные для персонажа]", 1)
        return None

    # Определяем роль персонажа
    role = "друг" if is_friend else "враг"

    # Включаем информацию о "relations" (отношении с игроком) в сообщение
    relations_info = character_data.get('relations', {}).get('master', 0.5)  # по умолчанию 0.5
    sys_msg = (
        f"Ты играешь в DnD. У тебя есть персонаж, и ты должен следовать его роли. Отвечай по 2-3 предложения максимум. "
        f"Ты {role} по имени {character_data['name']}. "
        f"Легенда: {character_data['legend']}. "
        f"Параметры: {character_data['params']}. "
        f"Взаимоотношение с игроком: {relations_info}. "
        f"Моральные принципы: {character_data['morals']}. "
        f"Настроение: {character_data['mood']}."
    )
    
    # Начинаем историю диалога
    conversation_history = [f"System: {sys_msg}"]

    stdscr.addstr(28, 0, f"Ты встретил {role}: {character_data['name']}.\n", curses.color_pair(4))
    stdscr.addstr(29, 0, f"Легенда: {character_data['legend']}\n", curses.color_pair(2))
    stdscr.refresh()

    count = 0
    try:
        interface = GameInterface(stdscr, rows)

        while True:
            user_input = get_user_input(stdscr, rows)
            if user_input.startswith('@run') or 'run!' in user_input.lower():
                stdscr.addstr("\nВы убежали!.\n", curses.color_pair(4))
                stdscr.refresh()
                break

            # Завершение диалога при нажатии Ctrl+S
            if user_input == '\x13':  # Ctrl+S
                stdscr.addstr("\nДиалог завершён.\n", curses.color_pair(4))
                stdscr.refresh()
                break

            # Проверка на специальные команды
            if user_input.startswith('@fight') or 'fight!' in user_input.lower():
                stdscr.addstr("\nВы решили начать битву!\n", curses.color_pair(1))
                stdscr.refresh()
                return start_battle(stdscr, character_data, player_stats, score)

            # Добавляем сообщение игрока в историю диалога
            conversation_history.append(f"User: {user_input}")
            
            # Генерация ответа от персонажа
            response = generate_npc_response(ai21, sys_msg, conversation_history)
            if not response:
                display_error(stdscr, "[Ошибка: Не удалось получить ответ.]", 1)
                continue

            # Оценка поведения игрока
            dialogue_score = evaluate_dialogue(user_input, character_data)

            # Добавляем ответ персонажа в историю и отображаем его
            conversation_history.append(f"Assistant: {response}")
            string = f"\n{response}\n"
            
            # Выводим ответ NPC в интерфейсе
            interface.draw_interface(string, character_data)

            stdscr.refresh()
            count += 1

    except KeyboardInterrupt:
        stdscr.addstr("\nДиалог прерван пользователем.\n", curses.color_pair(4))
        stdscr.refresh()

    # Если это враг, можно вернуть статус победы/поражения
    if not is_friend and player_stats and score is not None:
        return True, score + 100  # Враг побеждён, добавляем очки
    return None


def interact_with_treasure():
    return