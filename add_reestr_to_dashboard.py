# add_reestr_to_dashboard.py — 100% рабочая версия
import pandas as pd
import os
import glob
import re
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
data_js_path = os.path.join(current_dir, "data.js")

# Ищем любой файл reestr_companies*.xlsx
excel_files = glob.glob(os.path.join(current_dir, "reestr_companies*.xlsx"))
if not excel_files:
    print("Не найден файл reestr_companies*.xlsx в папке project!")
    exit()

excel_path = excel_files[0]
print(f"Найден файл: {os.path.basename(excel_path)}")

# Читаем Excel
df = pd.read_excel(excel_path)
print(f"Столбцы: {list(df.columns)}")

# Загружаем data.js как текст
if not os.path.exists(data_js_path):
    print("data.js не найден!")
    exit()

with open(data_js_path, "r", encoding="utf-8") as f:
    content = f.read()

# Ищем начало и конец массива companies
start = content.find("const companies = [")
end = content.rfind("];") + 2
if start == -1 or end <= start:
    print("Не найден массив companies в data.js")
    exit()

array_content = content[start+17:end-2].strip()  # вырезаем только внутри [ ... ]

# Разбиваем по строкам и парсим вручную (надёжно!)
existing_companies = []
lines = [line.strip() for line in array_content.splitlines() if line.strip() and line.strip() != ","]

for line in lines:
    if not line.startswith("{") or not line.endswith("},"):
        continue
    line = line[:-1]  # убираем запятую в конце
    # Парсим поля
    try:
        name_match = re.search(r'name:"([^"]*)"', line)
        inn_match = re.search(r'inn:"([^"]*)"', line)
        city_match = re.search(r'city:"([^"]*)"', line)
        revenue_match = re.search(r'revenue:"([^"]*)"', line)
        employees_match = re.search(r'employees:(\d+)', line)

        name = name_match.group(1) if name_match else "—"
        inn = inn_match.group(1) if inn_match else ""
        city = city_match.group(1) if city_match else "Калининград"
        revenue = revenue_match.group(1) if revenue_match else "0 млн"
        employees = int(employees_match.group(1)) if employees_match else 1

        existing_companies.append({"name": name, "inn": inn, "city": city, "revenue": revenue, "employees": employees, "accredited": True})
    except:
        continue  # если строка кривая — пропускаем

existing_inns = {c["inn"] for c in existing_companies if c["inn"] and c["inn"] != "—"}
print(f"Уже в базе: {len(existing_companies)} компаний")

# Города по ИНН
def get_city(inn):
    if not inn or len(inn) < 4:
        return "Россия"
    prefix = inn[:4]
    return "Калининград" if prefix.startswith("39") else "Россия"

# Добавляем новые компании
new_added = 0
for _, row in df.iterrows():
    inn = str(row.get("ИНН", "")).strip()
    if inn in ("nan", ""):
        inn = ""

    if inn and inn in existing_inns:
        continue  # дубликат

    name = str(row.get("Правообладатель", "")).strip()
    if not name or name == "nan":
        name = str(row.get("Название ПО", "")).strip()

    name = re.sub(r'\s+', ' ', name).strip()
    if not name or name == "nan":
        continue

    # Экранируем кавычки для JS
    name_js = name.replace('\\', '\\\\').replace('"', '\\"')

    city = get_city(inn)

    existing_companies.append({
        "name": name,
        "inn": inn or "—",
        "city": city,
        "revenue": "Нет данных",
        "employees": 1,
        "accredited": True
    })
    if inn:
        existing_inns.add(inn)
    new_added += 1

# Перезаписываем data.js
with open(data_js_path, "w", encoding="utf-8") as f:
    f.write("const companies = [\n")
    for c in existing_companies:
        f.write(f'  {{name:"{c["name"].replace('"', '\\"')}", inn:"{c["inn"]}", city:"{c["city"]}", revenue:"{c["revenue"]}", employees:{c["employees"]}, accredited:true}},\n')
    f.write("];\n")

print(f"\nУСПЕШНО!")
print(f"Добавлено новых компаний: {new_added}")
print(f"Всего в дашборде: {len(existing_companies)}")

print("\nПримеры добавленных из реестра:")
for c in existing_companies[-new_added:]:
    print(f"   • {c['name'][:70]:70} | {c['inn']}")