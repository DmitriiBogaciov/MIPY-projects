from collections import defaultdict, Counter
import statistics

class OneBetStrategy:
    def __init__(self, number, log_filename="bet_logs.txt"):
        self.initial_bank = 190000
        self.bank = self.initial_bank
        self.bet = 500
        self.number = str(number)  # храним как строку, чтобы сравнивать с '00'
        self.betting = True
        self.bet_stop = 20
        self.fall_count = 0
        self.spin_waiting = 25
        self.spin_count_before_bet = 0
        self.wins = 0
        self.losses = 0
        self.log_filename = log_filename  # Лог-файл

        # Запись в файл с заголовком
        with open(self.log_filename, 'w', encoding='utf-8') as log_file:
            log_file.write("Запуск стратегии на число: " + self.number + "\n")
            log_file.write("Начальный банк: 1000\n")
            log_file.write("Старт игры...\n")

    def parse_line(self, line):
        try:
            return line.strip().split('-')[-1].strip()
        except IndexError:
            return None

    def log(self, message):
        # Логируем каждое действие
        with open(self.log_filename, 'a', encoding='utf-8') as log_file:
            log_file.write(message + "\n")

    def play(self, input_filename):
        results = []

        try:
            with open(input_filename, 'r', encoding='utf-8') as f:
                for line in f:
                    number = self.parse_line(line)
                    if number in [str(n) for n in range(37)] + ['00']:
                        results.append(number)
        except FileNotFoundError:
            print(f"Файл '{input_filename}' не найден.")
            return

        if not results:
            print("В файле не найдено ни одного числа.")
            self.log("В файле не найдено ни одного числа.")
            return

        try:
            for number in results:
                self.spin_count_before_bet += 1

                if self.betting and self.spin_count_before_bet > self.spin_waiting:
                    self.log(f"🎯 Ставим. Спин {self.spin_count_before_bet}. Выпало число: {number}. Банк: {self.bank}")

                    if number == self.number:
                        self.bank += 35 * self.bet
                        self.wins += 1
                        self.fall_count = 0
                        self.log(f"✅ Выигрыш! Число {self.number} выпало. Банк после выигрыша: {self.bank}")

                        self.spin_count_before_bet = 0
                        self.log(f"⏸ Пауза после выигрыша на {self.spin_waiting} спинов.")
                    else:
                        self.bank -= self.bet
                        self.fall_count += 1
                        self.losses += 1
                        self.log(f"❌ Проигрыш. Число {number} не выпало. Банк после проигрыша: {self.bank}")

                        if self.fall_count >= self.bet_stop:
                            self.betting = False
                            self.spin_count_before_bet = 0
                            self.log(f"⛔ Прекращаем ставки после {self.fall_count} неудач. Ждём выпадения числа.")
                
                else: 
                    self.log(f"🎰 Спин {self.spin_count_before_bet}. Выпало число: {number}. Банк: {self.bank}")
                    if number == self.number:
                        self.betting = True
                        self.spin_count_before_bet = 0
                        self.fall_count = 0
                        self.log(f"▶️ Число {self.number} выпало. Возобновляем ставки.")

            # Статистика
            self.log("\n📊 Статистика:")
            self.log(f"Начальный банк: {self.initial_bank}")
            self.log(f"Конечный банк: {self.bank}")
            self.log(f"Выигрышей: {self.wins}")
            self.log(f"Проигрышей: {self.losses}")
            self.log(f"Чистая прибыль: {self.bank - self.initial_bank}")
        except Exception as e:
            self.log(f"Ошибка {e}")

# Интерактивный запуск
if __name__ == "__main__":
    input_filename = input("Введите имя входного файла (например, roulette_data.txt): ").strip()
    number = input("Введите число, на которое будем ставить (0–36 или 00): ").strip()
    log_filename = input("Введите имя файла для логов (например, bet_logs.txt): ").strip() or "bet_logs.txt"

    strategy = OneBetStrategy(number, log_filename)
    strategy.play(input_filename)
    print(f"Логи сохранены в файл: {log_filename}")