import random
import curses
from game.rules.game_over import game_over

def display_battle_info(stdscr, character_data, player_stats, player_health, enemy_health):
    """Отображает информацию о битве, включая параметры игрока и врага."""
    stdscr.clear()  # Очистить экран перед рисованием новой информации
    stdscr.addstr(f"Вы начали битву с врагом: {character_data['name']}!\n", curses.color_pair(1))
    stdscr.addstr("Битва началась!\n", curses.color_pair(3))
    stdscr.addstr("Параметры врага:\n", curses.color_pair(1))
    for param, value in character_data['params'].items():
        stdscr.addstr(f"{param.capitalize()}: {value} ", curses.color_pair(1))
        player_value = player_stats.get(param, 0)  # Если параметр не существует у игрока, то ставим 0
        stdscr.addstr(f"{player_value}\n", curses.color_pair(2))  # Зелёный цвет для игрока

    # Отображаем здоровье
    stdscr.addstr(f"\nВаше здоровье: {player_health}\n", curses.color_pair(4))
    stdscr.addstr(f"Здоровье врага: {enemy_health}\n", curses.color_pair(4))

    stdscr.refresh()  # Перерисовываем экран

def get_player_choice(stdscr):
    """Получает выбор игрока для атаки, защиты или побега."""
    stdscr.addstr("\n1. Атаковать. 2. Защититься. 3. Убежать\nВаш выбор: ", curses.color_pair(3))
    stdscr.refresh()
    return stdscr.getch()

def perform_attack(stdscr, player_stats, character_data, enemy_health):
    """Выполняет атаку игрока, обновляя здоровье врага с учетом экипированных предметов."""
    
    # Учитываем параметры с экипированных предметов
    weapon_bonus = 0
    if character_data['inventory']['equipped']['weapon']:
        weapon = character_data['inventory']['equipped']['weapon']
        weapon_bonus = weapon.get('effect', {}).get('strength', 0)

    player_roll = random.randint(1, 6) + player_stats.get('strength', 0) + weapon_bonus  # Урон с учетом оружия
    enemy_roll = random.randint(1, 6) + character_data['params'].get('strength', 0)
    
    # Показываем результат кубиков
    stdscr.addstr(f"Кубики: Враг: {enemy_roll} | Вы: {player_roll}\n", curses.color_pair(1))
    
    # Ожидаем результат атаки
    damage = max(0, player_roll - enemy_roll)
    enemy_health -= damage
    stdscr.addstr(f"\nВы нанесли врагу {damage} урона!\n", curses.color_pair(2))
    return enemy_health

def perform_defense(stdscr, player_stats, character_data, player_health):
    """Выполняет защиту игрока, обновляя здоровье игрока с учетом экипированных предметов."""
    
    # Учитываем бонусы от брони
    armor_bonus = 0
    if character_data['inventory']['equipped']['armor']:
        armor = character_data['inventory']['equipped']['armor']
        armor_bonus = armor.get('effect', {}).get('strength', 0)
    
    player_roll = random.randint(1, 6) + player_stats.get('strength', 0) + armor_bonus  # Защита с учетом брони
    enemy_roll = random.randint(1, 6) + character_data['params'].get('strength', 0)
    
    # Показываем результат кубиков
    stdscr.addstr(f"Кубики: Враг: {enemy_roll} | Вы: {player_roll}\n", curses.color_pair(3))
    
    # Ожидаем результат защиты
    blocked = max(0, player_roll - enemy_roll)
    player_health -= max(0, random.randint(5, 15) - blocked)
    stdscr.addstr(f"\nВы заблокировали {blocked} урона!\n", curses.color_pair(3))
    return player_health

def perform_enemy_attack(stdscr, player_stats, character_data, player_health):
    """Выполняет атаку врага, обновляя здоровье игрока с учетом экипированных предметов врага."""
    
    # Учитываем параметры с экипированных предметов врага
    enemy_weapon_bonus = 0
    if character_data['inventory']['equipped']['weapon']:
        enemy_weapon = character_data['inventory']['equipped']['weapon']
        enemy_weapon_bonus = enemy_weapon.get('effect', {}).get('strength', 0)

    enemy_roll = random.randint(1, 6) + character_data['params'].get('strength', 0) + enemy_weapon_bonus
    player_roll = random.randint(1, 6) + player_stats.get('strength', 0)
    
    # Показываем результат кубиков
    stdscr.addstr(f"Кубики: Враг: {enemy_roll} | Вы: {player_roll}\n", curses.color_pair(1))
    
    # Враг наносит урон
    damage = max(0, enemy_roll - player_roll)
    player_health -= damage
    stdscr.addstr(f"\nВраг нанес вам {damage} урона!\n", curses.color_pair(1))
    return player_health


def start_battle(stdscr, character_data, player_stats, score):
    """Основная функция для начала битвы с персонажем."""
    # Инициализация здоровья
    player_health = player_stats.get("endurance", 10) * 10
    enemy_health = character_data["params"]["endurance"] * 10

    # Отображаем информацию о битве
    display_battle_info(stdscr, character_data, player_stats, player_health, enemy_health)

    while player_health > 0 and enemy_health > 0:
        stdscr.move(16, 0)  # Перемещаем курсор в начало экрана
        stdscr.clrtoeol()  # Очищаем строку с начала до конца

        # Получаем выбор игрока
        key = get_player_choice(stdscr)

        # Интеллект: выводим один раз, до начала раунда
        stdscr.addstr(f"\n\nИнтеллект: {character_data['params']['intelligence']} vs {player_stats.get('intelligence', 0)}\n")

        if key == ord('1'):  # Атака
            enemy_health = perform_attack(stdscr, player_stats, character_data, enemy_health)
        elif key == ord('2'):  # Защита
            player_health = perform_defense(stdscr, player_stats, character_data, player_health)
        elif key == ord('3'):  # Убежать
            stdscr.addstr("\nВы сбежали из боя!\n", curses.color_pair(1))
            stdscr.refresh()
            return False, score  # Возвращаем флаг побега и текущий счёт

        # Атака врага
        if enemy_health > 0:
            player_health = perform_enemy_attack(stdscr, player_stats, character_data, player_health)

        # Обновляем информацию о битве
        display_battle_info(stdscr, character_data, player_stats, player_health, enemy_health)

        stdscr.refresh()

    # Завершение битвы
    if player_health <= 0:
        stdscr.addstr("\nВы проиграли бой!\n", curses.color_pair(1))
        game_over(stdscr, score)  # Вызываем функцию конца игры
        return False, score
    else:
        stdscr.addstr("\nВы победили врага!\n", curses.color_pair(2))
        score += 100  # Добавляем очки за победу
        return True, score
