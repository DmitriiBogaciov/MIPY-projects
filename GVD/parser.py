import requests
from bs4 import BeautifulSoup

url = "https://daily.heroeswm.ru/roulette/all.php"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Сохраняем числа (последние спины) в список, фильтруя строки с "нет времени"
numbers = []
for td in soup.find_all("td"):
    span = td.find("span")
    if span and span.text.strip():
        number = span.text.strip()
        if number.isdigit() or number == "00":  # поддержка зеро
            time = td.get("title", "нет времени")
            if time != "нет времени":  # фильтруем строки без времени
                numbers.append((time, number))

# Преобразуем "00" в 37, обычные числа в int
parsed_numbers = []
for time, number in numbers:
    if number == "00":
        parsed_numbers.append((time, 37))
    else:
        parsed_numbers.append((time, int(number)))


def find_last_repeats(data, max_interval=20):
    """
    Находит, сколько спинов назад было последнее повторение через N спинов (N от 1 до max_interval).
    """
    results = {}

    # Проходим от самого последнего элемента
    for interval in range(1, max_interval + 1):
        found = False
        for i in range(len(data) - 1):
            if data[i][1] == data[i + interval][1]:
                # Сколько спинов назад: расстояние от начала до i
                spins_ago = i  # число спинов назад от начала
                results[interval] = (spins_ago, data[i][1])  # добавляем число, которое повторилось
                found = True
                break
        if not found:
            results[interval] = None  # Нет таких повторов

    return results


# Печатаем результаты
print("🔁 Последние моментальные повторения:")
stats = find_last_repeats(parsed_numbers)
for interval, (spins_ago, number) in stats.items():
    if spins_ago is not None:
        print(f"Повтор через {interval} спинов: {number} был {spins_ago} спинов назад")
    else:
        print(f"Повтор через {interval} спинов: ❌ не найдено")
