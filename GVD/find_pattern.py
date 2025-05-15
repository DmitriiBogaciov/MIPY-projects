from collections import Counter

def parse_line(line):
    try:
        return line.strip().split('-')[-1].strip()
    except IndexError:
        return None

def parse_pattern(input_pattern):
    try:
        return list(map(int, input_pattern.strip().split()))
    except ValueError:
        print("Некорректные числа")
        return []

def find_all_patterns(filenames, pattern):
    next_numbers_counter = Counter()

    for filename in filenames:
        results = []

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    number = parse_line(line)
                    if number in [str(n) for n in range(37)] + ['00']:
                        results.append(100 if number == '00' else int(number))
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            continue

        found_any = False
        for i in range(len(results) - len(pattern)):
            if results[i:i + len(pattern)] == pattern:
                if i + len(pattern) < len(results):
                    next_number = results[i + len(pattern)]
                    display_number = '00' if next_number == 100 else next_number
                    next_numbers_counter[display_number] += 1
                    print(f"✅ Найдена последовательность в файле {filename} на позиции {i}. Следующее число: {display_number}")
                    found_any = True

        if not found_any:
            print(f"❌ Последовательность в файле {filename} не найдена.")

    print("\n📊 Частота следующих чисел после последовательности:")
    for number, count in next_numbers_counter.most_common():
        print(f"{number}: {count} раз(а)")
    print("🔍 Поиск завершен.")

if __name__ == "__main__":
    print("Нахождение исторической последовательности для N чисел")

    input_files_raw = input("Введите имена входных файлов через пробел: ").strip()
    input_files = input_files_raw.split()

    while True:
        input_pattern_raw = input("Введите числа последовательности через пробел (или 'exit' для выхода): ").strip()
        if input_pattern_raw.lower() == 'exit':
            print("Выход из программы.")
            break

        if not input_pattern_raw:
            print("Пустой шаблон! Попробуйте снова.")
            continue

        pattern = parse_pattern(input_pattern_raw)
        if pattern:
            find_all_patterns(input_files, pattern)
