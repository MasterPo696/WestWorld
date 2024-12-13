import json
import curses
import random
import logging
from game.game_over import game_over
from config import AI21_API_KEY
from llm.ai21 import LLMServiceAI21
from game.screen.drawing import setup_colors

def load_character_data(name):
    """Загружает данные персонажа из файла."""
    with open(f'game/characters/npc/{name}.json', 'r') as file:
        return json.load(file)


def start_battle(stdscr, character_data, player_stats, score):
    """Функция для начала драки с персонажем."""
    stdscr.clear()
    stdscr.addstr(f"Вы начали битву с врагом: {character_data['name']}!\n", curses.color_pair(1))
    stdscr.addstr(f"Параметры врага: {character_data['params']}\n", curses.color_pair(2))
    stdscr.addstr("Битва началась!\n", curses.color_pair(3))
    stdscr.refresh()

    # Пример базовой битвы
    player_health = player_stats.get("endurance", 10) * 10
    enemy_health = character_data["params"]["endurance"] * 10

    while player_health > 0 and enemy_health > 0:
        stdscr.addstr(f"\nВаше здоровье: {player_health}\n", curses.color_pair(4))
        stdscr.addstr(f"Здоровье врага: {enemy_health}\n", curses.color_pair(4))
        stdscr.addstr("\n1. Атаковать\n2. Защититься\n3. Убежать\nВаш выбор: ", curses.color_pair(3))
        stdscr.refresh()

        # Получаем выбор игрока
        key = stdscr.getch()
        if key == ord('1'):  # Атака
            damage = random.randint(5, 15)
            enemy_health -= damage
            stdscr.addstr(f"\nВы нанесли врагу {damage} урона!\n", curses.color_pair(2))
        elif key == ord('2'):  # Защита
            damage = random.randint(0, 10)
            player_health -= max(0, damage - 5)  # Уменьшение урона
            stdscr.addstr(f"\nВы заблокировали часть урона, получив {damage - 5}!\n", curses.color_pair(3))
        elif key == ord('3'):  # Убежать
            stdscr.addstr("\nВы сбежали из боя!\n", curses.color_pair(1))
            return False, score  # Возвращаем флаг побега и текущий счёт

        # Атака врага
        if enemy_health > 0:
            damage = random.randint(5, 15)
            player_health -= damage
            stdscr.addstr(f"\nВраг нанес вам {damage} урона!\n", curses.color_pair(1))

    # Завершение битвы
    if player_health <= 0:
        stdscr.addstr("\nВы проиграли бой!\n", curses.color_pair(1))
        game_over(stdscr)  # Вызываем функцию конца игры
        return False, score
    else:
        stdscr.addstr("\nВы победили врага!\n", curses.color_pair(2))
        score += 100  # Добавляем очки за победу
        return True, score


def interact_with_character(stdscr, character_name, is_friend, player_stats, score):
    """Обрабатывает взаимодействие с персонажем (друг или враг)."""
    ai21 = LLMServiceAI21()  # Инициализация AI21 сервиса

    setup_colors()  # Настройка цветов для curses

    try:
        character_data = load_character_data(character_name)
    except FileNotFoundError:
        stdscr.addstr("[Ошибка: Не удалось загрузить данные для персонажа]\n", curses.color_pair(1))
        stdscr.refresh()
        return None

    # Формирование начального системного сообщения
    role = "друг" if is_friend else "враг"
    sys_msg = (f"Ты играешь в DnD. У тебя есть персонаж, и ты должен следовать его роли. Отвечай по 2-3 предложения максимум."
               f"Ты {role} по имени {character_data['name']}. "
               f"Легенда: {character_data['legend']}. "
               f"Параметры: {character_data['params']}. "
               f"Моральные принципы: {character_data['morals']}. "
               f"Настроение: {character_data['mood']}.")
    conversation_history = [f"System: {sys_msg}"]

    # Приветствие персонажа
    stdscr.addstr(f"Ты встретил {role}: {character_data['name']}.\n", curses.color_pair(4))
    stdscr.addstr(f"Легенда: {character_data['legend']}\n", curses.color_pair(2))
    stdscr.refresh()

    try:
        while True:
            # Получаем пользовательский ввод
            stdscr.addstr("\nВаше сообщение (Ctrl+S для завершения): ", curses.color_pair(3))
            stdscr.refresh()
            curses.echo()
            user_input = stdscr.getstr().decode('utf-8', errors='ignore').strip()
            curses.noecho()

            # Завершение диалога при нажатии Ctrl+S
            if user_input == '\x13':  # Ctrl+S
                stdscr.addstr("\nДиалог завершён.\n", curses.color_pair(4))
                stdscr.refresh()
                break

            # Проверка на специальные команды
            if user_input.startswith('@fight') or 'fight!' in user_input.lower():
                stdscr.addstr("\nВы решили начать битву!\n", curses.color_pair(1))
                return start_battle(stdscr, character_data, player_stats, score)

            # Добавляем сообщение игрока в историю диалога
            conversation_history.append(f"User: {user_input}")

            # Генерация ответа от персонажа
            response = ai21.generate_response(sys_msg, "\n".join(conversation_history))
            if not response:
                stdscr.addstr("[Ошибка: Не удалось получить ответ.]\n", curses.color_pair(1))
                stdscr.refresh()
                continue

            # Добавляем ответ персонажа в историю и отображаем его
            conversation_history.append(f"Assistant: {response}")
            stdscr.addstr(f"\n{character_data['name']} отвечает: {response}\n", curses.color_pair(1))
            stdscr.refresh()

    except KeyboardInterrupt:
        stdscr.addstr("\nДиалог прерван пользователем.\n", curses.color_pair(4))
        stdscr.refresh()

    # Если это враг, можно вернуть статус победы/поражения
    if not is_friend and player_stats and score is not None:
        return True, score + 100  # Враг побеждён, добавляем очки
    return None
