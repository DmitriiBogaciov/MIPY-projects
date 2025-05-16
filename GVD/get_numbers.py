def get_latest_numbers():
    import requests
    from bs4 import BeautifulSoup

    url = "https://daily.heroeswm.ru/roulette/all.php"
    try:
        response = requests.get(url, timeout=10)  # timeout на случай подвисаний
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Ошибка запроса к сайту: {e}")
        return []  # или можешь вернуть последние сохранённые числа, если хранишь их

    parsed_numbers = []
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        for td in soup.find_all("td"):
            span = td.find("span")
            if span and span.text.strip():
                number = span.text.strip()
                if number.isdigit() or number == "00":
                    time = td.get("title", "нет времени")
                    if time != "нет времени":
                        parsed_numbers.append(number)
    except Exception as e:
        print(f"❌ Ошибка парсинга страницы: {e}")
        return []

    return parsed_numbers
