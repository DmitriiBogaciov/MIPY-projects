def get_latest_numbers():
    import requests
    from bs4 import BeautifulSoup

    url = "https://daily.heroeswm.ru/roulette/all.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    parsed_numbers = []
    for td in soup.find_all("td"):
        span = td.find("span")
        if span and span.text.strip():
            number = span.text.strip()
            if number.isdigit() or number == "00":
                time = td.get("title", "нет времени")
                if time != "нет времени":
                    parsed_numbers.append(number)  # ВСЕГДА строка!

    return parsed_numbers