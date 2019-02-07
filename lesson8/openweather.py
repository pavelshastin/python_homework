
""" 
== OpenWeatherMap ==

OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.

Необходимо решить следующие задачи:

== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.
    
    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID, 
    используя дополнительную библиотеку GRAB (pip install grab)

        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up

        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in

        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys
        
        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

        
== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz
    
    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка 
     (воспользоваться модулем gzip 
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)
    
    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}
    
    
== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a

    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a

    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a


    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}    


== Сохранение данных в локальную БД ==    
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):

    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных

2. Выводить список стран из файла и предлагать пользователю выбрать страну 
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))

3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.


При работе с XML-файлами:

Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с пространствами имен удобно пользоваться такими функциями:

    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''

    tree = ET.parse(f)
    root = tree.getroot()

    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}

    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...

"""

import xml.etree.ElementTree as ET
import urllib.request
import gzip
import os
import json
import sqlite3
import re
import csv
import msvcrt

cities_file = "cities.json"
db_file = "weather.sqlite"
api_key_file = "app.id"
country_code_file = "country_code.csv"

city_list_url = "http://bulk.openweathermap.org/sample/city.list.json.gz"
country_codes_url = 'https://datahub.io/core/country-list/r/data.csv'

api_key = ""
with open(api_key_file, "r", encoding="UTF-8") as f:
    api_key = f.read().strip()

print(api_key)


req_city = urllib.request.Request(city_list_url)

if os.path.exists(cities_file) == False:
    print("Loading...")
    with open(cities_file, "wb") as f:
        with urllib.request.urlopen(req_city) as response:
            f.write(gzip.decompress(response.read()))


if os.path.exists(country_code_file) == False:
    with open(country_code_file, "wb") as f:
        with urllib.request.urlopen(country_codes_url) as response:
            read = response.read()
            try:
                f.write(gzip.decompress(read))
            except OSError:
                f.write(read)


if os.path.exists(db_file) == False:
    f = open(db_file, "w", encoding="UTF-8")
    f.close()





w_cities = ""
with open(cities_file, "r", encoding="UTF-8") as f:
    w_cities = f.read()

w_country_codes = set(re.findall(r"\"country\": \"([A-Z]+)\",", w_cities))
w_city_names = re.findall(r"\"id\":\s*(\d+),\s*\"name\":\s*\"([\w\s]+)\",\s*\"country\":\s*\"(\w+)\",\s*", w_cities)

country_names = {}
with open(country_code_file, "r", encoding="UTF-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        name, code = row.items()
        country_names[code[1]] = name[1]



chosen_countries = []
c_codes = list(country_names.keys())
per_page = 20
page_num = 0
c_code = ""

#print(c_codes)
#print(w_country_codes)
#print(w_city_names)

# while True:
#     cont = False
#     brk = False
#
#     if c_code in w_country_codes:
#         chosen_countries.append(c_code)
#
#     while True:
#         os.system('cls' if os.name == 'nt' else 'clear')
#
#         if len(chosen_countries) != 0:
#             print("Chosen: ", chosen_countries)
#
#         page = c_codes[page_num:page_num + per_page]
#
#         for c in page:
#             print(c, country_names[c])
#
#         inp = input("(-p/-n swap page -e exit)  Enter code of country like 'RU': ").strip().title()
#
#         if inp == "-P":
#             page_num = page_num - per_page if (page_num - per_page) >= 0 else 0
#             continue
#
#         if inp == "-N":
#             page_num = page_num + per_page
#             continue
#
#         if len(inp) == 2:
#             c_code = inp
#             cont = True
#             break
#
#         if inp == "Exit":
#             brk = True
#             break
#
#     if brk is True:
#         break
#     if cont is True:
#         continue
#
# print("Chosen countries: ", chosen_countries)


chosen_countries = ["RU", "US", "AF"]

cities_of_chosen_countries = list(filter(lambda c: c[2] in chosen_countries, w_city_names))


cities_of_chosen_countries.sort(key=lambda c: c[1])
chosen_cities = []

per_page = 10
page_num = 0
c_code = ""


# for country in chosen_countries:
#     cities_of_country_init = [(c[0], c[1]) for c in cities_of_chosen_countries if country in c]
#
#     os.system('cls' if os.name == 'nt' else 'clear')
#
#
#     cities_of_country = cities_of_country_init
#     while True:
#         os.system('cls' if os.name == 'nt' else 'clear')
#
#         if len(chosen_cities) != 0:
#             print("Chosen cities: ", chosen_cities)
#
#         page = cities_of_country[page_num:page_num + per_page]
#
#         for c in page:
#             print(c[0], c[1])
#
#         print("Choose city in the country of {}".format(country_names[country]))
#         inp = input("(-n/-p swap page -e exit -ns new search TYPE SOME LETTER TO FILTER) Enter full code of city: ").strip().title()
#
#         if inp == "-P":
#             page_num = page_num - per_page if (page_num - per_page) >= 0 else 0
#             continue
#
#         if inp == "-N":
#             page_num = page_num + per_page
#             continue
#
#         if inp == "-Ns":
#             cities_of_country = cities_of_country_init
#
#         if inp != "-P" and inp != "-N" and inp != "-E":
#             print(inp)
#             cs = list(filter(lambda c: c[1].startswith(inp), cities_of_country[:]))
#             if len(cs) != 0:
#                 cities_of_country = cs
#
#         if inp == "-E":
#             break
#
#         try:
#             inp = int(inp)
#             city_id = list(filter(lambda c: c[0] == str(inp), cities_of_country_init))[0]
#
#             if city_id:
#                 chosen_cities.append(city_id)
#
#             continue
#         except ValueError:
#             pass


#print(chosen_cities)
chosen_cities = [('5128581', 'New York'), ('1127768', 'Aibak')]

city_id_url = "http://api.openweathermap.org/data/2.5/group?id={}&units=metric&appid={}"\
                .format(",".join([c[0] for c in chosen_cities]), api_key)

print(city_id_url)

weather = ""
with urllib.request.urlopen(city_id_url) as response:
    weather = json.loads(response.read())

print(json.dumps(weather, indent=" "))