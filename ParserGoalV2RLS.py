from gettext import find
from pickle import NONE
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
    base_farm.execute('CREATE TABLE IF NOT EXISTS lekarstva(Remedy_id INTEGER PRIMARY KEY NOT NULL, Name_lp TEXT INTEGER, Active TEXT INTEGER, ATH TEXT INTEGER, Farm_group TEXT INTEGER, Sostav TEXT INTEGER, Description TEXT INTEGER, Farm_deystv TEXT INTEGER, Farmakodinamika TEXT INTEGER, Farmakokinetika TEXT INTEGER, Pokazaniya TEXT INTEGER, Protiv TEXT INTEGER, Pregnancy_lact TEXT INTEGER, Bad_effects TEXT INTEGER, Interaction TEXT INTEGER, Peredoz TEXT INTEGER, Osob_ukaz TEXT INTEGER, Forma_vipuska TEXT INTEGER, Proizvoditel TEXT INTEGER, Recept TEXT INTEGER, Save TEXT INTEGER, Srok TEXT INTEGER, Link TEXT INTEGER )')
    base_farm.commit()
farmdata_start() # запускам функцию с бд препаратов

headers = {"User-Agent":
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"}
#headers - заголовок, который считает парсируемый сервер, чтобы нас не вычислили
list_url = []

request_tuple_Link = cur_farm.execute('SELECT Link FROM "lekarstva"') # получаю список ссылок из бд
tuple_Link = cur_farm.fetchall() # вытаскиваю все ссылки в виде кортежа
for links in tuple_Link: # цикл для получения всех ссылок в распакованном виде
    links, = links # тут сама распаковочка
    
    sleep(0.5) # чтобы не улететь в бан делаем перерыв в 3 секунды
    
    answer_parser = requests.get(links, headers=headers) # ответ сервера на запрос по ссылке с фальш хэдером
    print(answer_parser) 

    soup = BeautifulSoup(answer_parser.text, "lxml") # lxml обрабатывает спаршенные данные в более адекватную вещь, но это объект супа
    
# паршу активное вещество
    try:
        soupActive = soup.find("h2", "structure-heading", "deistvuyushhee-veshhestvo", "Действующее вещество").next_sibling.next_sibling.text # тег, класс, айди, текст. следующий брат х2 в тексте
        soupActive = soupActive.strip() # убираю пробелы
        soupActive = re.sub(r'\([^()]*\)', '', soupActive) # убираю слова в скобках
        soupActive = soupActive.replace('*','') # убираю звездочку из строки
        soupActive = soupActive.strip() # снова убираю пробелы 
        cur_farm.execute('UPDATE "lekarstva" SET Active = ? WHERE Link = ?', (soupActive, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Active = ? WHERE Link = ?', ("Нет информации", links))

# паршу ATH РАБОТАЕТ!!!
    try:
        soupATH = soup.find("a", "js-anchor", "#atx", "ATX").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET ATH = ? WHERE Link = ?', (soupATH, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET ATH = ? WHERE Link = ?', ("Нет информации", links))
# паршу Farm_group
    try:
        soupFarm_group = soup.find("a", "js-anchor", "#farmakologiceskaya-gruppa", "Фармакологическая группа").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Farm_group = ? WHERE Link = ?', (soupFarm_group, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Farm_group = ? WHERE Link = ?', ("Нет информации", links))
# паршу Sostav
    try:
        soupSostav = soup.find("a", "js-anchor", "#sostav-i-forma-vypuska", "Состав и форма выпускa").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Sostav = ? WHERE Link = ?', (soupSostav, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Sostav = ? WHERE Link = ?', ("Нет информации", links))
# паршу Description
    try:
        soupDescription = soup.find("a", "js-anchor", "#opisanie-lekarstvennoi-formy", "Описание лекарственной формы").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Description = ? WHERE Link = ?', (soupDescription, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Description = ? WHERE Link = ?', ("Нет информации", links))
# паршу Farm_deystv
    try:
        soupFarm_deystv = soup.find("a", "js-anchor", "#farmakologiceskoe-deistvie", "Фармакологическое действие").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Farm_deystv = ? WHERE Link = ?', (soupFarm_deystv, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Farm_deystv = ? WHERE Link = ?', ("Нет информации", links))
# паршу Farmakodinamika
    try:
        soupFarmakodinamika = soup.find("a", "js-anchor", "#farmakodinamika", "Фармакодинамика").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Farmakodinamika = ? WHERE Link = ?', (soupFarmakodinamika, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Farmakodinamika = ? WHERE Link = ?', ("Нет информации", links))
# паршу Farmakokinetika
    try:
        soupFarmakokinetika = soup.find("a", "js-anchor", "#farmakokinetika", "Фармакокинетика").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Farmakokinetika = ? WHERE Link = ?', (soupFarmakokinetika, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Farmakokinetika = ? WHERE Link = ?', ("Нет информации", links))
# паршу Pokazaniya
    try:
        soupPokazaniya = soup.find("a", "js-anchor", "#pokazaniya", "Показания").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Pokazaniya = ? WHERE Link = ?', (soupPokazaniya, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Pokazaniya = ? WHERE Link = ?', ("Нет информации", links))
# паршу Protiv
    try:
        soupProtiv = soup.find("a", "js-anchor", "#protivopokazaniya", "Противопоказания").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Protiv = ? WHERE Link = ?', (soupProtiv, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Protiv = ? WHERE Link = ?', ("Нет информации", links))
# паршу Pregnancy_lact
    try:
        soupPregnancy_lact = soup.find("a", "js-anchor", "#primenenie-pri-beremennosti-i-kormlenii-grudyu", "Применение при беременности и кормлении грудью").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Pregnancy_lact = ? WHERE Link = ?', (soupPregnancy_lact, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Pregnancy_lact = ? WHERE Link = ?', ("Нет информации", links))
# паршу Bad_effects
    try:
        soupBad_effects = soup.find("a", "js-anchor", "#pobocnye-deistviya", "Побочные действия").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Bad_effects = ? WHERE Link = ?', (soupBad_effects, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Bad_effects = ? WHERE Link = ?', ("Нет информации", links))
# паршу Interaction
    try:
        soupInteraction = soup.find("a", "js-anchor", "#vzaimodeistvie", "Взаимодействие").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Interaction = ? WHERE Link = ?', (soupInteraction, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Interaction = ? WHERE Link = ?', ("Нет информации", links))
# паршу Sposob
    try:
        soupSposob = soup.find("a", "js-anchor", "#sposob-primeneniya-i-dozy", "Способ применения и дозы").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Sposob = ? WHERE Link = ?', (soupSposob, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Sposob = ? WHERE Link = ?', ("Нет информации", links))
# паршу Peredoz
    try:
        soupPeredoz = soup.find("a", "js-anchor", "#peredozirovka", "Передозировка").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Peredoz = ? WHERE Link = ?', (soupPeredoz, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Peredoz = ? WHERE Link = ?', ("Нет информации", links))
# паршу Osob_ukaz
    try:
        soupOsob_ukaz = soup.find("a", "js-anchor", "#osobye-ukazaniya", "Особые указания").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Osob_ukaz = ? WHERE Link = ?', (soupOsob_ukaz, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Osob_ukaz = ? WHERE Link = ?', ("Нет информации", links))
# паршу Forma_vipuska
    try:
        soupForma_vipuska = soup.find("a", "js-anchor", "#forma-vypuska", "Форма выпуска").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Forma_vipuska = ? WHERE Link = ?', (soupForma_vipuska, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Forma_vipuska = ? WHERE Link = ?', ("Нет информации", links))
# паршу Proizvoditel
    try:
        soupProizvoditel = soup.find("a", "js-anchor", "#proizvoditel", "Производитель").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Proizvoditel = ? WHERE Link = ?', (soupProizvoditel, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Proizvoditel = ? WHERE Link = ?', ("Нет информации", links))
# паршу Recept
    try:
        soupRecept = soup.find("a", "js-anchor", "#usloviya-otpuska-iz-aptek", "Условия отпуска из аптек").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Recept = ? WHERE Link = ?', (soupRecept, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Recept = ? WHERE Link = ?', ("Нет информации", links))
# паршу Save
    try:
        soupSave = soup.find("a", "js-anchor", "#usloviya-xraneniya", "Условия хранения").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Save = ? WHERE Link = ?', (soupSave, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Save = ? WHERE Link = ?', ("Нет информации", links))
# паршу Srok
    try:
        soupSrok = soup.find("a", "js-anchor", "#srok-godnosti", "Срок годности").get("href")
        cur_farm.execute('UPDATE "lekarstva" SET Srok = ? WHERE Link = ?', (soupSrok, links))
    except:
        cur_farm.execute('UPDATE "lekarstva" SET Srok = ? WHERE Link = ?', ("Нет информации", links))

    base_farm.commit()