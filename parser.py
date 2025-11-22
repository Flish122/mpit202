import requests
from bs4 import BeautifulSoup
import openpyxl

# Создаём новый Excel-файл
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Компании"
ws.append(["Название", "ИНН", "ОГРН", "Деятельность"])

# Функция парсинга одной страницы
def parse_page(page_num):
    url = f"https://www.1cont.ru/contragent/by-region/kaliningradskaya-oblast?page={page_num}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка загрузки страницы {page_num}: статус {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("div.contragent-item")

    print(f"Страница {page_num}: найдено компаний — {len(items)}")

    for item in items:
        try:
            name = item.select_one("div.contragent-title a")
            inn = item.select_one("div.contragent-inn")
            ogrn = item.select_one("div.contragent-ogrn")
            activity = item.select_one("div.contragent-activity")

            ws.append([
                name.text.strip() if name else "",
                inn.text.strip() if inn else "",
                ogrn.text.strip() if ogrn else "",
                activity.text.strip() if activity else ""
            ])
        except Exception as e:
            print(f"Ошибка при обработке компании: {e}")

# Цикл по страницам (например, первые 5)
for page in range(1, 6):
    parse_page(page)

# Сохраняем Excel-файл
wb.save("companies.xlsx")
print("✅ Данные сохранены в companies.xlsx")
