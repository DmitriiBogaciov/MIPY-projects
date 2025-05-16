from collections import deque, Counter

class DynamicHotNumbersBot:
    def __init__(self, initial_bank=500000, min_hot_count=2, history_len=50, top_n=4, bet=500):
        self.initial_bank = initial_bank
        self.bank = initial_bank
        self.history = deque(maxlen=history_len)
        self.min_hot_count = min_hot_count
        self.top_n = top_n
        self.bet = bet

    def get_hot_numbers(self):
        counter = Counter(self.history)
        hot_candidates = [(num, count) for num, count in counter.items() if count >= self.min_hot_count]
        hot_candidates.sort(key=lambda x: (-x[1], x[0]))
        hot_numbers = [num for num, _ in hot_candidates[:self.top_n]]
        return set(hot_numbers)

    def simulate_on_file(self, filepath, logpath):
        with open(filepath, encoding='utf-8') as f:
            data = [
                int(part.strip())
                for line in f
                if (part := line.strip().split('-')[-1].strip()).isdigit()
            ]

        with open(logpath, 'w', encoding='utf-8') as log:
            for i, number in enumerate(data):
                hot_numbers = self.get_hot_numbers()
                log.write(f"[{i}] Выпало: {number} | Динамический топ: {sorted(hot_numbers)} | ")
                if hot_numbers:
                    self.bank -= len(hot_numbers) * self.bet
                    log.write(f"🎯 Ставка на {sorted(hot_numbers)}. Выпало {number}. ")
                    if number in hot_numbers:
                        win = self.bet * 36
                        self.bank += win
                        profit = win - (len(hot_numbers) * self.bet)
                        log.write(f"✅ Победа! +{profit} | Банк: {self.bank}\n")
                    else:
                        log.write(f"Мимо | Банк: {self.bank}\n")
                else:
                    log.write("Нет горячих чисел, пропуск ставки.\n")
                self.history.append(number)

        return self.bank

# Интерактивный запуск
if __name__ == "__main__":
    print("🎯 Симуляция ДИНАМИЧЕСКОЙ стратегии горячих чисел")
    filepath = input("Введите имя файла с данными (например, data.txt): ").strip()
    logpath = input("Введите имя файла для логов (например, dynamic_hot_log.txt): ").strip()

    bot = DynamicHotNumbersBot(top_n=4)  # например, топ-4
    final_bank = bot.simulate_on_file(filepath, logpath)
    print(f"Окончательный банк: {final_bank}")
