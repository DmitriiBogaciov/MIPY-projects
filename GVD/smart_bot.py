from collections import deque, Counter

class HotNumbersBot:
    def __init__(self, initial_bank=1000, min_hot_count=2, history_len=50, max_attempts=10):
        self.initial_bank = initial_bank
        self.bank = initial_bank
        self.history = deque(maxlen=history_len)
        self.min_hot_count = min_hot_count   # Сколько раз число должно выпасть за history_len спинов, чтобы быть "горячим"
        self.max_attempts = max_attempts
        self.betting = False
        self.bet_targets = set()
        self.bet_attempts = 0

    def reset(self):
        self.betting = False
        self.bet_targets = set()
        self.bet_attempts = 0

    def get_hot_numbers(self):
        # Считаем числа за последние N спинов
        counter = Counter(self.history)
        # Горячие числа — те, что выпали хотя бы min_hot_count раз
        hot_numbers = {num for num, count in counter.items() if count >= self.min_hot_count}
        return hot_numbers

    def simulate_on_file(self, filepath, logpath):
        with open(filepath, encoding='utf-8') as f:
            data = [
                int(part.strip())
                for line in f
                if (part := line.strip().split('-')[-1].strip()).isdigit()
            ]

        with open(logpath, 'w', encoding='utf-8') as log:
            for i, number in enumerate(data):
                self.history.append(number)
                log.write(f"[{i}] Выпало: {number} | ")

                # Определяем горячие числа
                hot_numbers = self.get_hot_numbers()
                log.write(f"Горячие числа: {sorted(hot_numbers)} | ")

                # Если не ставим, начинаем, если есть горячие числа
                if not self.betting and hot_numbers:
                    self.bet_targets = set(hot_numbers)
                    self.betting = True
                    self.bet_attempts = 0
                    log.write(f"🚨 Начинаем ставить на: {sorted(self.bet_targets)}\n")
                    continue

                # Ставим на все горячие числа
                if self.betting:
                    self.bank -= len(self.bet_targets)  # одна ставка на каждое горячее число
                    self.bet_attempts += 1
                    log.write(f"🎯 Ставка на {sorted(self.bet_targets)}. Выпало {number}. ")

                    if number in self.bet_targets:
                        win = 36
                        self.bank += win
                        log.write(f"✅ Победа! +{win - 1 * len(self.bet_targets)} | Банк: {self.bank}\n")
                        self.reset()
                    elif self.bet_attempts >= self.max_attempts:
                        log.write(f"❌ Превышено число попыток. Сброс. | Банк: {self.bank}\n")
                        self.reset()
                    else:
                        log.write(f"Мимо | Попытка {self.bet_attempts}/{self.max_attempts} | Банк: {self.bank}\n")

        return self.bank

# Интерактивный запуск
if __name__ == "__main__":
    print("🎯 Симуляция стратегии по горячим числам")
    filepath = input("Введите имя файла с данными (например, data.txt): ").strip()
    logpath = input("Введите имя файла для логов (например, hot_numbers_log.txt): ").strip()

    bot = HotNumbersBot()
    final_bank = bot.simulate_on_file(filepath, logpath)
    print(f"Окончательный банк: {final_bank}")
