from collections import defaultdict, Counter
import statistics

def parse_line(line):
    try:
        return line.strip().split('-')[-1].strip()
    except IndexError:
        return None

def analyze_intervals(results, max_interval=10):
    last_seen = {}
    interval_occurrences = defaultdict(list)  # interval -> list of (index, number)

    for index, number in enumerate(results):
        if number in last_seen:
            interval = index - last_seen[number]
            if 1 <= interval <= max_interval:
                interval_occurrences[interval].append(index)
        last_seen[number] = index

    interval_stats = {}

    for interval, positions in interval_occurrences.items():
        if len(positions) < 2:
            continue
        # Разница между позициями с одинаковым интервалом
        gaps = [positions[i] - positions[i - 1] for i in range(1, len(positions))]
        interval_stats[interval] = {
            "count": len(positions),
            "gaps": gaps,
            "mean": statistics.mean(gaps) if gaps else 0,
            "min": min(gaps) if gaps else 0,
            "max": max(gaps) if gaps else 0
        }

    return interval_stats

def analyze_roulette_file(input_filename, output_filename):
    results = []

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                number = parse_line(line)
                if number in [str(n) for n in range(37)] + ['00']:
                    results.append(number)
    except FileNotFoundError:
        print(f"Файл '{input_filename}' не найден.")
        return

    if not results:
        print("В файле не найдено ни одного числа.")
        return

    stats = Counter(results)
    total_spins = sum(stats.values())

    interval_analysis = analyze_intervals(results, max_interval=10)

    try:
        with open(output_filename, 'w', encoding='utf-8') as out:
            out.write(f"Всего спинов: {total_spins}\n\n")

            out.write("Статистика выпадений (число: количество раз, %):\n")
            for number, count in sorted(stats.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 37):
                percent = (count / total_spins) * 100
                out.write(f"{number}: {count} ({percent:.2f}%)\n")

            out.write("\nАнализ повторов с коротким интервалом (1–10 спинов):\n")
            for interval in range(1, 11):
                data = interval_analysis.get(interval)
                if data:
                    out.write(f"\n📌 Интервал {interval}:\n")
                    out.write(f"  Повторов с таким интервалом: {data['count']}\n")
                    out.write(f"  Между этими повторами:\n")
                    out.write(f"    ➤ Средний промежуток: {data['mean']:.2f} спинов\n")
                    out.write(f"    ➤ Минимальный: {data['min']} спинов\n")
                    out.write(f"    ➤ Максимальный: {data['max']} спинов\n")
                else:
                    out.write(f"\n📌 Интервал {interval}:\n  Нет повторов с таким интервалом.\n")

        print(f"\n✅ Подробная статистика сохранена в файл: {output_filename}")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

# Интерактивный запуск
if __name__ == "__main__":
    print("📊 Расширенный анализ интервалов повторов чисел (1–10)")

    input_filename = input("Введите имя входного файла (например, roulette_data.txt): ").strip()
    output_filename = input("Введите имя выходного файла (например, stats.txt): ").strip()

    analyze_roulette_file(input_filename, output_filename)
