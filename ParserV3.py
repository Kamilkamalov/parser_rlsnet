import re
import requests
from bs4 import BeautifulSoup
from time import sleep

import sqlite3

def farmdata_start(): # БД
    global base_farm, cur_farm
    base_farm = sqlite3.connect('farmdata.db')
    cur_farm = base_farm.cursor()
    if base_farm:
        print('База данных препаратов существует')
    else:
        print('База данных препаратов либо не существует, либо к ней невозможно подключиться')
    base_farm.execute('CREATE TABLE IF NOT EXISTS lekarstva(Remedy_id INTEGER PRIMARY KEY NOT NULL, Name_lp TEXT INTEGER, Active TEXT INTEGER, ATH TEXT INTEGER, Farm_group TEXT INTEGER, Sostav TEXT INTEGER, Description TEXT INTEGER, Farm_deystv TEXT INTEGER, Farmakodinamika TEXT INTEGER, Farmakokinetika TEXT INTEGER, Pokazaniya TEXT INTEGER, Protiv TEXT INTEGER, Pregnancy_lact TEXT INTEGER, Bad_effects TEXT INTEGER, Interaction TEXT INTEGER, Sposob TEXT INTEGER, Peredoz TEXT INTEGER, Osob_ukaz TEXT INTEGER, Forma_vipuska TEXT INTEGER, Proizvoditel TEXT INTEGER, Recept TEXT INTEGER, Save TEXT INTEGER, Srok TEXT INTEGER, Link TEXT INTEGER )')
    base_farm.commit()
farmdata_start() # запускам функцию с бд препаратов

headers = {"User-Agent":
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"}
#headers - заголовок, который считает парсируемый сервер, чтобы нас не вычислили

list_url = [] # Это будущий список, в который добавятся данные из второго цикла for на 45 строке

all_pages = ["/c0", "/c1", "/c2", "/c3", "/c4", "/c5", "/c6", "/c7", "/c8", "/c9", "/ca", "/cb", "/cc", "/cd", "/ce", "/cf", "/d0", "/d1", "/d2", "/d3", "/d4", "/d5", "/d6", "/d7", "/d8", "/dd", "/de", "/df", "/1"]
for all_pages in all_pages: # все страницы 
    sleep(3) # чтобы не улететь в бан делаем перерыв в 3 секунды
    url = f'https://www.rlsnet.ru/drugs/ukazatel{all_pages}' # ссылка с которой копируем и count - ссылка на нужну страницу
    parser = requests.get(url, headers=headers)
    print(parser)

    file = open("Parser.txt", "w+")
    file.write(parser.text) # спаршенная html страница
    file.close()

    soup = BeautifulSoup(parser.text, "lxml") # lxml обрабатывает спаршенные данные в более адекватную вещь, но это объект супа

    links = soup.find_all("div", "item") # беру первым <div>, а потом уточняю класс "item"
    
    #active = soup.find_all("div", "item")
    
    
    for item in links: # цикл для создания списка
        
        item_text = item.text.strip() # отрезаю пробелы у названий лп
        item_text = re.sub(r'\([^()]*\)', '', item_text) # регулярное выражение, которое удаляет всё что есть в скобках, кроме других подстрок, которые еще в одних скобках))
        item_text = item_text.strip()
        item_text = item_text.replace('®', '')
        item_text = item_text.replace('™', '')
    #    item_url = item.find("a").get("href") # выцепляю <href> из всех <a>, соответствующих параметрам в links
        item_url = item.find("a")['href']
        cur_farm.execute('INSERT INTO lekarstva (Name_lp, Link) VALUES(?, ?)', (item_text, item_url)) # вставляю спаршенные данные в бд
        list_url.append(item_url) # добавляю в конец списка последнюю ссылку из цикла, пока цикл активен
        print(f"{item_text}: {item_url}")

        base_farm.commit()

    # item_Name_lp = cur_farm.execute('SELECT Link FROM "lekarstva" WHERE Name_lp = ?', (item_text)) # беру из бд названия лекарств
    
