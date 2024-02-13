import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

requests.packages.urllib3.disable_warnings()

all_data = []
current_dateTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
base_url = "https://carpis.ru/oem_parts/benson/"
page_num = 1

while True:
    url = base_url + "?PAGEN_1=page-" + str(page_num)
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    if page_num == 171:
        break

    num = 0
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        row_data_new = [item.replace('\n', ',') for item in row_data]
        row_data_new1 = [item.replace('\r', ',') for item in row_data_new]
        row_data_new2 = [item.replace('\t', ',') for item in row_data_new1]
        row_data_new3 = [re.sub(r',+', ',', item) for item in row_data_new2]
        data.append(row_data_new3)
        data_split = [row[0].split(',') for row in data]
        # print(row)
    
    all_data.extend(data_split)
    page_num += 1

if all_data:
    df = pd.DataFrame(all_data, names=['Бренд', 'OEM', 'Наименоание', 'Предложений', 'Мин. цена'])
    output_path = 'data/table' + str(current_dateTime) + '.xlsx'  # Путь к файлу Excel
    df.to_excel(output_path, index=False, header=False)
else:
    print("Нет данных на сайте")