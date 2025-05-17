from collections import deque, Counter
import matplotlib.pyplot as plt
import numpy as np

class DynamicHotNumbersBot:
    def __init__(self, initial_bank=500000, min_hot_count=2, history_len=50, top_n=4, bet=3500):
        self.initial_bank = initial_bank
        self.bank = initial_bank
        self.real_bank = initial_bank
        self.max_bank = initial_bank 
        self.history = deque(maxlen=history_len)
        self.min_hot_count = min_hot_count        
        self.top_n = top_n
        self.bet = bet
        self.max_loss_bank = 0.9
        self.in_pause = False

    def get_hot_numbers(self):
        counter = Counter(self.history)
        hot_candidates = [(num, count) for num, count in counter.items() if count >= self.min_hot_count]
        hot_candidates.sort(key=lambda x: (-x[1], x[0]))
        hot_numbers = [num for num, _ in hot_candidates[:self.top_n]]
        return set(hot_numbers)

    def simulate_on_file(self, filepath, logpath):
        banks_over_time = []
        real_bank_over_time = []
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
                
                if not self.in_pause:
                    self.real_bank = self.bank
                    if self.bank > self.max_bank: 
                        self.max_bank = self.bank
                    if self.bank < self.max_bank*self.max_loss_bank:
                        self.in_pause = True
                else:
                    if self.bank >= self.max_bank*self.max_loss_bank:
                        self.in_pause = False
                
                self.history.append(number)
                banks_over_time.append(self.bank)
                real_bank_over_time.append(self.real_bank)

        
        plt.figure(figsize=(12,6))
        plt.plot(banks_over_time, label='Банк')
        plt.plot(real_bank_over_time, label='Реал')
        plt.xlabel("Номер спина")
        plt.ylabel("Банк")
        plt.title("Баланс по стратегии горячих чисел (динамический топ)")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

        return self.bank

# Интерактивный запуск
if __name__ == "__main__":
    print("🎯 Симуляция ДИНАМИЧЕСКОЙ стратегии горячих чисел")
    filepath = input("Введите имя файла с данными (например, data.txt): ").strip()
    logpath = input("Введите имя файла для логов (например, dynamic_hot_log.txt): ").strip()

    bot = DynamicHotNumbersBot(top_n=4)  # например, топ-4
    final_bank = bot.simulate_on_file(filepath, logpath)
    print(f"Окончательный банк: {final_bank}")
