import requests
from bs4 import BeautifulSoup
from time import sleep
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active


inpp = input("Введіть назву товару: ")
cina = int(input("Введіть мінімальну ціну: "))
for count in range(1, 5):
    url = f'https://www.olx.ua/uk/list/q-{inpp}' #посилання на сайт
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all("div", class_="css-1sw7q4x")

    for i in data:
        name = i.find("h6", class_="css-16v5mdi er34gjf0")
        all_links = i.find("a", class_="css-rc5s2u")
        price = i.find('p', class_="css-10b0gli er34gjf0")

            # Перевірте, чи знайдено дані перед додаванням до Excel-таблиці
        if name and all_links and price:
            name = name.text
            price_text = price.text

            # Вилучте символи коми та пробіли і перетворіть ціну у числовий формат
            price_value = float(''.join(price_text.split()[:-1]).replace(',', ''))

            # Перевірте, чи ціна не менше 10 тисяч
            if price_value >= cina:
                link = 'https://www.olx.ua/' + all_links['href']
                print(name + '\n' + price_text + '\n' + link + '\n')

                # Додайте дані до Excel-таблиці
                row_data = [name, price_text, link]
                ws.append(row_data)

    # Перевірте, чи є дані перед збереженням Excel-файлу
if ws.max_row > 1:
    wb.save('ooo.xlsx')
    print('Дані збережено в ooo.xlsx')
else:
    print('Дані не знайдено для збереження')