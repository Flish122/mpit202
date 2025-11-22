# add_from_your_table.py  ← сохрани как новый файл
import pandas as pd
import os
import re

# Пути
current_dir = os.path.dirname(os.path.abspath(__file__))
data_js_path = os.path.join(current_dir, "data.js")
excel_path = os.path.join(current_dir, "companies_with_accreditation.xlsx")

if not os.path.exists(excel_path):
    print("Не найден файл companies_with_accreditation.xlsx в текущей папке!")
    exit()

if not os.path.exists(data_js_path):
    print("Не найден data.js в текущей папке!")
    exit()

print("Читаем твою таблицу компаний...")
df = pd.read_excel(excel_path)

# Читаем текущий data.js и собираем все существующие ИНН
with open(data_js_path, "r", encoding="utf-8") as f:
    content = f.read()

existing_inns = set(re.findall(r'inn:"([^"]*)"', content))

new_lines = []
added = 0

print("Обрабатываем строки...")
for _, row in df.iterrows():
    name = str(row["Название"]).strip()
    inn = str(row["ИНН"]).strip() if pd.notna(row["ИНН"]) else ""

    if name in ("nan", "") or name == "Название":  # пропускаем заголовок и пустые
        continue

    if inn and inn in existing_inns:
        continue  # уже есть — не дублируем

    # Определяем город/регион (по первым цифрам ИНН или по адресу)
    if inn.startswith("39"):
        city = "Калининград"
    elif pd.notna(row.get("Адрес")) and "москва" in str(row["Адрес"]).lower():
        city = "Москва"
    elif pd.notna(row.get("Адрес")) and "краснодар" in str(row["Адрес"]).lower():
        city = "Краснодар"
    else:
        city = "Россия"

    name_clean = name.replace('"', '\\"').replace("\n", " ")
    
    new_line = f'  {{name:"{name_clean}", inn:"{inn or "—"}", city:"{city}", revenue:"Нет данных", employees:1, accredited:true}},\n'
    new_lines.append(new_line)
    
    if inn:
        existing_inns.add(inn)
    added += 1

if added == 0:
    print("Новых компаний не найдено — все уже есть в data.js")
    exit()

# Вставляем перед последним ];
insert_pos = content.rfind("];")
if insert_pos == -1:
    print("Ошибка: не найден конец массива в data.js")
    exit()

new_content = content[:insert_pos] + "".join(new_lines) + content[insert_pos:]

with open(data_js_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"ГОТОВО! Добавлено {added} новых компаний из твоей таблицы")
print("Обнови страницу с дашбордом — увидишь МТС, Тандер (Магнит), Дикси, РТРС и всех остальных в списке аккредитованных")# add_from_your_table.py  ← сохрани как новый файл
import pandas as pd
import os
import re

# Пути
current_dir = os.path.dirname(os.path.abspath(__file__))
data_js_path = os.path.join(current_dir, "data.js")
excel_path = os.path.join(current_dir, "companies_with_accreditation.xlsx")

if not os.path.exists(excel_path):
    print("Не найден файл companies_with_accreditation.xlsx в текущей папке!")
    exit()

if not os.path.exists(data_js_path):
    print("Не найден data.js в текущей папке!")
    exit()

print("Читаем твою таблицу компаний...")
df = pd.read_excel(excel_path)

# Читаем текущий data.js и собираем все существующие ИНН
with open(data_js_path, "r", encoding="utf-8") as f:
    content = f.read()

existing_inns = set(re.findall(r'inn:"([^"]*)"', content))

new_lines = []
added = 0

print("Обрабатываем строки...")
for _, row in df.iterrows():
    name = str(row["Название"]).strip()
    inn = str(row["ИНН"]).strip() if pd.notna(row["ИНН"]) else ""

    if name in ("nan", "") or name == "Название":  # пропускаем заголовок и пустые
        continue

    if inn and inn in existing_inns:
        continue  # уже есть — не дублируем

    # Определяем город/регион (по первым цифрам ИНН или по адресу)
    if inn.startswith("39"):
        city = "Калининград"
    elif pd.notna(row.get("Адрес")) and "москва" in str(row["Адрес"]).lower():
        city = "Москва"
    elif pd.notna(row.get("Адрес")) and "краснодар" in str(row["Адрес"]).lower():
        city = "Краснодар"
    else:
        city = "Россия"

    name_clean = name.replace('"', '\\"').replace("\n", " ")
    
    new_line = f'  {{name:"{name_clean}", inn:"{inn or "—"}", city:"{city}", revenue:"Нет данных", employees:1, accredited:true}},\n'
    new_lines.append(new_line)
    
    if inn:
        existing_inns.add(inn)
    added += 1

if added == 0:
    print("Новых компаний не найдено — все уже есть в data.js")
    exit()

# Вставляем перед последним ];
insert_pos = content.rfind("];")
if insert_pos == -1:
    print("Ошибка: не найден конец массива в data.js")
    exit()

new_content = content[:insert_pos] + "".join(new_lines) + content[insert_pos:]

with open(data_js_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"ГОТОВО! Добавлено {added} новых компаний из твоей таблицы")
print("Обнови страницу с дашбордом — увидишь МТС, Тандер (Магнит), Дикси, РТРС и всех остальных в списке аккредитованных")