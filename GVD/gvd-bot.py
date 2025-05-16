import pyautogui
import keyboard
import threading
import random
import time
from datetime import datetime

# Словарь координат для каждого числа
BET_POSITIONS_SIWA = {
    38: (407, 312),
    37: (409, 346),
    0: (406, 275),
    1: (457, 359),
    2: (456, 311),
    3: (457, 262),
    4: (507, 360),
    5: (505, 310),
    6: (505, 263),
    7: (552, 358),
    8: (552, 313),
    9: (552, 260),
    10: (601, 357),
    11: (601, 310),
    12: (601, 262),
    13: (648, 359),
    14: (648, 310),
    15: (648, 260),
    16: (696, 357),
    17: (696, 310),
    18: (696, 260),
    19: (744, 360),
    20: (744, 310),
    21: (744, 260),
    22: (794, 360),
    23: (794, 310),
    24: (794, 260),
    25: (840, 360),
    26: (840, 310),
    27: (840, 260),
    28: (889, 360),
    29: (889, 310),
    30: (889, 260),
    31: (937, 360),
    32: (937, 310),
    33: (937, 260),
    34: (985, 360),
    35: (985, 310),
    36: (985, 260),
}

BET_POSITIONS = {
    37: (408, 328),
    00: (406, 259),
    1: (455, 341),
    2: (456, 295),
    3: (457, 247),
    4: (507, 341),
    5: (505, 295),
    6: (505, 247),
    7: (552, 341),
    8: (552, 295),
    9: (552, 247),
    10: (601, 341),
    11: (601, 295),
    12: (601, 247),
    13: (648, 341),
    14: (648, 295),
    15: (648, 247),
    16: (696, 341),
    17: (696, 295),
    18: (696, 247),
    19: (744, 341),
    20: (744, 295),
    21: (744, 247),
    22: (794, 341),
    23: (794, 295),
    24: (794, 247),
    25: (840, 341),
    26: (840, 295),
    27: (840, 247),
    28: (889, 341),
    29: (889, 295),
    30: (889, 247),
    31: (937, 341),
    32: (937, 295),
    33: (937, 247),
    34: (985, 341),
    35: (985, 295),
    36: (985, 247),
}

# Координаты кнопки "Крутить рулетку"
BET_BUTTON1 = (491, 544)
BET_BUTTON2 = (439, 605)

ROULETE_BUTTON = (772, 176)
ROLE_HISTORY_CLICK = (768, 291)

# Флаг работы бота
running = False
bet_numbers = []  # Список для 5 чисел
bot_thread = None  # Поток бота

# Горячая клавиша для старта/остановки
TOGGLE_HOTKEY = "f6"

# Индекс текущего числа и счётчик прокрутов для каждого числа
current_bet_index = 0
spin_count = 0


def random_delay(min_time=0.8, max_time=1.5):
    """Случайная задержка для имитации человеческого поведения"""
    return random.uniform(min_time, max_time)


def click(x, y):
    """Кликаем по указанным координатам с небольшим отклонением"""
    x += random.randint(-2, 2)
    y += random.randint(-2, 2)
    pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.5))
    time.sleep(random_delay(0.8, 1.5))
    pyautogui.click()
    time.sleep(random_delay(0.8, 1.5))


def place_bet(bet_number):
    """Ставит ставку на указанное число"""
    if bet_number not in BET_POSITIONS_SIWA:
        print(f"❌ Координаты для числа {bet_number} не заданы!")
        return
    
    x, y = BET_POSITIONS_SIWA[bet_number]
    print(f"🎰 Ставка на {bet_number} ({x}, {y})")
    click(x, y)


def confirm_bet():
    """Подтверждает ставку, нажимая на две кнопки"""
    click(*BET_BUTTON1)
    click(*BET_BUTTON2)


def refresh_page():
    """Обновляет страницу в браузере"""
    pyautogui.hotkey("command", "r")  # Для macOS


def move_to_history(): 
    x, y = ROULETE_BUTTON
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.5))
    time.sleep(random.uniform(1, 2))  # Небольшая пауза перед кликом
    pyautogui.click(*ROLE_HISTORY_CLICK)


def move_to_roulette(): 
    click(*ROULETE_BUTTON)
    click(180, 459)

def wait_until_next_bet_time():
    """Ждёт до ближайшего момента вида xx:06, xx:11, xx:16 и т.д."""
    now = datetime.now()
    # Следующее время = ближайшее кратное 5 минутам + 1 минута (то есть xx:06, xx:11 и т.д.)
    minutes = ((now.minute // 5) + 1) * 5 + 1
    if minutes >= 60:
        next_time = now.replace(hour=(now.hour + 1) % 24, minute=minutes % 60, second=0, microsecond=0)
    else:
        next_time = now.replace(minute=minutes, second=0, microsecond=0)

    wait_time = (next_time - now).total_seconds()
    print(f"🕒 Ждём до следующего времени ставки: {next_time.strftime('%H:%M:%S')} (через {int(wait_time)} сек.)")
    time.sleep(wait_time)


def bot_loop():
    """Основной цикл бота, работает в фоновом потоке"""
    global running, bet_numbers, current_bet_index, spin_count
    
    while running:
        for bet_number in bet_numbers:
            place_bet(bet_number)
            confirm_bet()
            time.sleep(random_delay(5, 6))
        move_to_history()
        wait_until_next_bet_time()
        time.sleep(random_delay(20, 40)) # Задержка до следующего прокрута
        refresh_page()
        time.sleep(random_delay(5, 6))  # Задержка между действиями
        move_to_roulette()
        refresh_page()
        time.sleep(random_delay(5, 6))


def toggle_bot():
    """Включает/выключает бота"""
    global running, bot_thread

    running = not running
    if running:
        print(f"✅ Бот запущен. Бот будет ставить числа по очереди: {bet_numbers}")
        bot_thread = threading.Thread(target=bot_loop, daemon=True)
        bot_thread.start()
    else:
        print("⏹️ Бот остановлен")


def start_bot():
    global bet_numbers
    while True:
        try:
            bet_numbers_input = input("Введите чисела, на которые ставить (через пробел): ")
            bet_numbers = list(map(int, bet_numbers_input.split()))
            if any(num not in BET_POSITIONS_SIWA for num in bet_numbers):
                print("❌ Введите корректные чисела (от 0 до 36)!")
                continue
            break
        except ValueError:
            print("❌ Введите корректные числа!")

    print(f"🔄 Запускаем бота, нажми {TOGGLE_HOTKEY} для старта/остановки.")
    keyboard.add_hotkey(TOGGLE_HOTKEY, toggle_bot)
    keyboard.wait()  # Ждём нажатий клавиш


# Запускаем бота
start_bot()