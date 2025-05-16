import pyautogui
import keyboard
import threading
import random
import time
from collections import Counter
import get_numbers
from datetime import datetime
import os

class HotNumbersBot:
    def __init__(self,
                 history_len=50,
                 min_hot_count=2,
                 top_n=4,
                 delay_range=(0.8, 1.5),
                 hotkey="f6",
                 bet_amount=500,
                 profit_file="profit_state.txt"
                 ):
        self.history_len = history_len
        self.min_hot_count = min_hot_count
        self.top_n = top_n
        self.delay_range = delay_range
        self.hotkey = hotkey
        self.bet_amount = bet_amount
        self.profit_file = profit_file
        self.profit = self.load_profit()
        

        self.running = False
        self.bot_thread = None

        # координаты
        self.BET_POSITIONS_SIWA = {
            "00": (409, 346),
            "0": (406, 275),
            "1": (457, 359),
            "2": (456, 311),
            "3": (457, 262),
            "4": (507, 360),
            "5": (505, 310),
            "6": (505, 263),
            "7": (552, 358),
            "8": (552, 313),
            "9": (552, 260),
            "10": (601, 357),
            "11": (601, 310),
            "12": (601, 262),
            "13": (648, 359),
            "14": (648, 310),
            "15": (648, 260),
            "16": (696, 357),
            "17": (696, 310),
            "18": (696, 260),
            "19": (744, 360),
            "20": (744, 310),
            "21": (744, 260),
            "22": (794, 360),
            "23": (794, 310),
            "24": (794, 260),
            "25": (840, 360),
            "26": (840, 310),
            "27": (840, 260),
            "28": (889, 360),
            "29": (889, 310),
            "30": (889, 260),
            "31": (937, 360),
            "32": (937, 310),
            "33": (937, 260),
            "34": (985, 360),
            "35": (985, 310),
            "36": (985, 260),
        }
        self.BET_BUTTON1 = (491, 544)
        self.BET_BUTTON2 = (439, 605)
        self.ROULETE_BUTTON = (772, 176)
        self.ROLE_HISTORY_CLICK = (768, 291)
        
    def load_profit(self):
        if os.path.exists(self.profit_file):
            with open(self.profit_file, 'r', encoding='utf-8') as f:
                value = f.read().strip()
                try: 
                    return int(value)
                except Exception: 
                    pass
        return 0
    
    def save_profit(self): 
        with open(self.profit_file, 'w', encoding='utf-8') as f:
            f.write(str(self.profit))

    def random_delay(self):
        return random.uniform(*self.delay_range)

    def click(self, x, y):
        x += random.randint(-2, 2)
        y += random.randint(-2, 2)
        pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.5))
        time.sleep(self.random_delay())
        pyautogui.click()
        time.sleep(self.random_delay())

    def place_bet(self, bet_number):
        if bet_number not in self.BET_POSITIONS_SIWA:
            print(f"❌ Координаты для числа {bet_number} не заданы!")
            return
        x, y = self.BET_POSITIONS_SIWA[bet_number]
        print(f"🎰 Ставка на {bet_number} ({x}, {y})")
        self.click(x, y)

    def confirm_bet(self):
        self.click(*self.BET_BUTTON1)
        self.click(*self.BET_BUTTON2)

    def refresh_page(self):
        pyautogui.hotkey("command", "r")

    def move_to_history(self):
        x, y = self.ROULETE_BUTTON
        x += random.randint(-5, 5)
        y += random.randint(-5, 5)
        pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.5))
        time.sleep(random.uniform(1, 2))
        pyautogui.click(*self.ROLE_HISTORY_CLICK)

    def move_to_roulette(self):
        self.click(*self.ROULETE_BUTTON)
        self.click(180, 459)

    def wait_until_next_bet_time(self):
        now = datetime.now()
        minutes = ((now.minute // 5) + 1) * 5 + 1
        if minutes >= 60:
            hour = (now.hour + 1) % 24
            minute = minutes % 60
            next_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if hour == 0 and now.hour == 23:
                # Новый день: добавить сутки
                next_time += timedelta(days=1)
        else:
            next_time = now.replace(minute=minutes, second=0, microsecond=0)

        wait_time = (next_time - now).total_seconds()
        if wait_time < 0:
            # Safety, вдруг что-то не так
            wait_time = 0
        time.sleep(wait_time)

    def get_numbers_from_source(self):
        return get_numbers.get_latest_numbers()

    def get_hot_numbers(self, numbers):
        if not numbers:
            print('Не удалось получить свежие числа')
            return []
        history = numbers[:self.history_len]
        counter = Counter(history)
        hot_candidates = [(num, count) for num, count in counter.items() if count >= self.min_hot_count]
        hot_candidates.sort(key=lambda x: (-x[1], int(x[0])))  # если хочешь по числу, не по строке!
        hot_numbers = [num for num, _ in hot_candidates[:self.top_n]]
        print("Горячие числа: ", hot_numbers)
        return hot_numbers

    def bot_loop(self):
        with open('hot_numbers_log.txt', 'a', encoding='utf-8') as log:
            while self.running:
                numbers = self.get_numbers_from_source()
                hot_numbers = self.get_hot_numbers(numbers)
                if not hot_numbers:
                    print("Нет горячих чисел, жду минуту...")
                    time.sleep(60)
                    continue
                print(f"🔥 Актуальные горячие числа: {hot_numbers}")

                for bet_number in hot_numbers:
                    self.place_bet(bet_number)
                    # self.confirm_bet()
                    time.sleep(self.random_delay())
                self.move_to_history()

                self.wait_until_next_bet_time()
                time.sleep(random.uniform(20, 40))
                self.refresh_page()
                time.sleep(self.random_delay())
                self.move_to_roulette()
                self.refresh_page()
                time.sleep(self.random_delay())

                latest_numbers = self.get_numbers_from_source()
                latest_result = latest_numbers[0] if latest_numbers else None

                # Профит за раунд
                total_bet = len(hot_numbers) * self.bet_amount
                win = latest_result in hot_numbers
                if win:
                    win_amount = self.bet_amount * 36
                    round_profit = win_amount - total_bet
                else:
                    round_profit = -total_bet
                self.profit += round_profit
                self.save_profit()

                log_entry = (
                    f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                    f"Горячие числа: {hot_numbers} | "
                    f"Выпало: {latest_result} | "
                    f"{'✅ Победа' if win else '❌ Мимо'} | "
                    f"Профит: {round_profit} | Суммарный профит: {self.profit}\n"
                )
                print(log_entry.strip())
                log.write(log_entry)
                log.flush()

    def toggle_bot(self):
        self.running = not self.running
        if self.running:
            print(f"✅ Бот запущен.")
            self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
            self.bot_thread.start()
        else:
            print("⏹️ Бот остановлен")

    def start_bot(self):
        print(f"🔄 Запускаем бота, нажми {self.hotkey} для старта/остановки.")
        keyboard.add_hotkey(self.hotkey, self.toggle_bot)
        keyboard.wait()

# ----
if __name__ == "__main__":
    bot = HotNumbersBot()
    bot.start_bot()
