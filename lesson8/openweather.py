# =*= coding: utf-8 =*=
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


import urllib.request
import gzip
import os
import json
import sqlite3
import re
import csv
from datetime import datetime as dt


api_key_file = "app.id"
db_file = "weather.sqlite"


#Creating database
if os.path.exists(db_file) == False:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE weather (city_id integer primary key, name text, "
                   "date text, temp integer, weather_ids text)")
    conn.commit()


api_key = ""
with open(api_key_file, "r", encoding="UTF-8") as f:
    api_key = f.read().strip()


#print(api_key)

#If there is a file with previously chosen cities, we give User a list of options via Input(...
# -p use previously chosen cities
# -a add new cities to the existing list
# -n create new list of cities

chosen_cities = []

if os.path.exists("chosen_cities.json"):
    with open("chosen_cities.json", "r", encoding="UTF-8") as f:
        chosen_cities = json.loads(f.read())

inp = ""
if len(chosen_cities) != 0:
    print("Chosen cities: ", chosen_cities)
    inp = input("Do you want to proceed with chosen cities(-p)/add others(-a)/choose new(-n): ").strip().title()


#If User has chosen ADD or NEW list
if inp == "-A" or inp == "-N" or inp == "":

    #If New list
    if inp == "-N":
        chosen_cities = []

    # Automation of whole city list attriving from openweathermap.org
    # where country is given with its code like 'RU' or 'US'
    cities_file = "cities.json"


    city_list_url = "http://bulk.openweathermap.org/sample/city.list.json.gz"


    req_city = urllib.request.Request(city_list_url)

    if os.path.exists(cities_file) == False:
        print("Loading...")
        with open(cities_file, "wb") as f:
            with urllib.request.urlopen(req_city) as response:
                f.write(gzip.decompress(response.read()))


    #Automation of country names - country codes list from datahub.io
    country_codes_url = 'https://datahub.io/core/country-list/r/data.csv'
    country_code_file = "country_code.csv"

    if os.path.exists(country_code_file) == False:
        with open(country_code_file, "wb") as f:
            with urllib.request.urlopen(country_codes_url) as response:
                read = response.read()
                try:
                    f.write(gzip.decompress(read))
                except OSError:
                    f.write(read)

    #Parsing city names and country codes from openweathermap.org  city-file
    w_cities = ""
    with open(cities_file, "r", encoding="UTF-8") as f:
        w_cities = f.read()

    w_country_codes = set(re.findall(r"\"country\": \"([A-Z]+)\",", w_cities))
    w_city_names = re.findall(r"\"id\":\s*(\d+),\s*\"name\":\s*\"([\w\s]+)\",\s*\"country\":\s*\"(\w+)\",\s*", w_cities)

    #Creating dictionary {country_code: country_name}
    country_names = {}
    with open(country_code_file, "r", encoding="UTF-8") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)

        for row in reader:
            name, code = row
            country_names[code] = name

    print(country_names)

    # Interface for choosing countries with pagination. The program prints a list of countries
    # <Country code>, <Country name> devided into pages.
    # User can getting through pages via commands:
    # -n next page
    # -p previous page
    # -e exit
    # User choose the country and put its CODE into input line.

    chosen_countries = []
    c_codes = sorted(list(country_names.keys()))
    per_page = 10  #items per page
    page_num = 0   #initial page number
    c_code = ""

    #print(c_codes)
    #print(w_country_codes)
    #print(w_city_names)

    while True:
        cont = False
        brk = False

        #Checking if an inserted country code exists in codes, retrieved from openweather.org
        if c_code in w_country_codes:
            chosen_countries.append(c_code)

        while True:
            #Clearing terminal
            os.system('cls' if os.name == 'nt' else 'clear')

            #printing already chosen countries
            if len(chosen_countries) != 0:
                print("Chosen: ", chosen_countries)

            #slicing country codes for current page
            page = c_codes[page_num:page_num + per_page]

            for code in page:
                print(code, country_names[code])

            inp = input("(-p/-n swap page -e exit)  Enter code of country like 'RU': ").strip().upper()
            #print(inp)

            #Checking control commands
            if inp == "-P":
                page_num = page_num - per_page if (page_num - per_page) >= 0 else 0
                continue

            if inp == "-N":
                page_num = page_num + per_page
                continue

            if inp == "-E":
                print("in", inp)
                brk = True
                break

            #If user's input equals to 2-letters code of country
            if len(inp) == 2:
                c_code = inp
                cont = True
                break


        if brk is True:
            break
        if cont is True:
            continue

    print("Chosen countries: ", chosen_countries)


    #Creating a list of cities in chosen countries, recieved from openweather.org
    cities_of_chosen_countries = list(filter(lambda c: c[2] in chosen_countries, w_city_names))

    cities_of_chosen_countries.sort(key=lambda c: c[1])



    # Interface for choosing cities with pagination and filtering. The program prints a list of cities
    # <city id>, <city name> devided into pages.
    # User can getting through pages via commands:
    # -n next page
    # -p previous page
    # -e exit
    #
    # User can insert only begining of city name (like mos for Moscow) and the program will print
    # consequent list of cities.
    #
    # -ms brings the city list to the initial state (Whole city list) to begin new search
    #
    # User choose the city and put its ID into input line.
    #
    # After User has finished choosing city of a current country, enter -e to go to the NEXT country
    # city chose.
    per_page = 10
    page_num = 0
    c_code = ""

    #Chosen countries iteration to choose cities country by country
    for country in chosen_countries:

        #List of current country cities
        cities_of_country_init = [(c[0], c[1]) for c in cities_of_chosen_countries if country in c]

        os.system('cls' if os.name == 'nt' else 'clear')


        cities_of_country = cities_of_country_init

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            if len(chosen_cities) != 0:
                print("Chosen cities: ", chosen_cities)

            page = cities_of_country[page_num:page_num + per_page]

            for city in page:
                print(city[0], city[1]) #<City id> <City name>

            print("Choose city in the country of {}".format(country_names[country]))

            inp = input("(-n/-p swap page -e exit -ns new search TYPE SOME LETTER TO FILTER) Enter full code of city: ")\
                    .strip().title()


            # Checking control commands
            if inp == "-P":
                page_num = page_num - per_page if (page_num - per_page) >= 0 else 0
                continue

            elif inp == "-N":
                page_num = page_num + per_page
                continue

            elif inp == "-Ns":
                page_num = 0
                cities_of_country = cities_of_country_init
                continue

            elif inp == "-E":
                break

            elif inp != "-P" and inp != "-N" and inp != "-E":

                #Filtering city list to match only a part of city name given by user.
                cs = list(filter(lambda c: c[1].startswith(inp), cities_of_country[:]))

                if len(cs) != 0:
                    cities_of_country = cs
                    page_num = 0
                    continue

                #If User has input integer number (city code).
                try:
                    inp = int(inp)

                    #If city code exists in city list from openweather.org
                    city_id = list(filter(lambda c: c[0] == str(inp), cities_of_country_init))[0]

                    if city_id:
                        chosen_cities.append(city_id)

                    continue
                except (ValueError, IndexError):
                    pass

    #Storing chosen list of cities into file
    with open("chosen_cities.json", "w") as f:
        f.write(json.dumps(chosen_cities, indent="  "))


#print(chosen_cities)


#Reciving data from openweather.org via its API
city_id_url = "http://api.openweathermap.org/data/2.5/group?id={c_ids}&units=metric&appid={key}"\
                .format(c_ids=",".join([c[0] for c in chosen_cities]), key=api_key)

#print(city_id_url)

#Storing retrived data to temp file (Lunix)
weather = ""
with open("temp.json", "wb") as f:
    with urllib.request.urlopen(city_id_url) as response:
        f.write(response.read())

with open("temp.json", "r", encoding="UTF-8") as f:
    weather = json.loads(f.read())

#print(json.dumps(weather, indent=" "))

#Formating recieved data to match DB requirements (5 fileds)
city_weather = [(w['id'],
                 w['name'],
                 dt.fromtimestamp(w['dt']).isoformat(sep=" "),  #Converting epoch seconds to literal date
                 int(w['main']['temp']),
                 ";".join([str('{}, {}'.format(img['id'], img['icon'])) for img in w['weather']])
                 ) for w in weather['list']]

#print(city_weather)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

city_ids_in_db = [id[0] for id in cursor.execute("SELECT city_id FROM weather")]
#print(city_ids_in_db)

#
for w in city_weather:
    if w[0] in city_ids_in_db:

        cursor.execute("""
            UPDATE weather 
            SET temp='{t}', date='{d}', weather_ids='{w_ids}'
            WHERE city_id = '{c_id}'
        """.format(t=w[3], d=w[2], w_ids=w[4], c_id=w[0]))
    else:

        cursor.execute("INSERT INTO weather VALUES (?,?,?,?,?)", w)

conn.commit()
conn.close()

print("Current weather data has been load to database")