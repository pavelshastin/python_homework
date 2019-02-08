


cities_file = "cities.json"
db_file = "weather.sqlite"
api_key_file = "app.id"
country_code_file = "country_code.csv"

city_list_url = "http://bulk.openweathermap.org/sample/city.list.json.gz"
country_codes_url = 'https://datahub.io/core/country-list/r/data.csv'

api_key = ""
with open(api_key_file, "r", encoding="UTF-8") as f:
    api_key = f.read().strip()

#print(api_key)

chosen_cities = []

if os.path.exists("chosen_cities.json"):
    with open("chosen_cities.json", "r", encoding="UTF-8") as f:
        chosen_cities = json.loads(f.read())


if len(chosen_cities) != 0:
    print("Chosen cities: ", chosen_cities)
    inp = input("Do you want to proceed with chosen cities(-C)/add others(-A)/choose new(-N) ")



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

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE weather (city_id integer primary key, name text, "
                "date text, temp integer, weather_ids text)")

    conn.commit()




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
#
#         inp = input("(-n/-p swap page -e exit -ns new search TYPE SOME LETTER TO FILTER) Enter full code of city: ")\
#                 .strip().title()
#
#         if inp == "-P":
#             page_num = page_num - per_page if (page_num - per_page) >= 0 else 0
#             continue
#
#         elif inp == "-N":
#             page_num = page_num + per_page
#             continue
#
#         elif inp == "-Ns":
#             page_num = 0
#             cities_of_country = cities_of_country_init
#             continue
#
#         elif inp == "-E":
#             break
#
#         elif inp != "-P" and inp != "-N" and inp != "-E":
#
#             cs = list(filter(lambda c: c[1].startswith(inp), cities_of_country[:]))
#
#             if len(cs) != 0:
#                 cities_of_country = cs
#                 page_num = 0
#                 continue
#
#             try:
#                 inp = int(inp)
#                 city_id = list(filter(lambda c: c[0] == str(inp), cities_of_country_init))[0]
#
#                 if city_id:
#                     chosen_cities.append(city_id)
#
#                 continue
#             except (ValueError, IndexError):
#                 pass



#print(chosen_cities)
with open("chosen_cities.json", "w") as f:
    f.write(json.dumps(chosen_cities, indent="  "))


city_id_url = "http://api.openweathermap.org/data/2.5/group?id={}&units=metric&appid={}"\
                .format(",".join([c[0] for c in chosen_cities]), api_key)

print(city_id_url)

weather = ""
with open("temp.json", "wb") as f:
    with urllib.request.urlopen(city_id_url) as response:
        f.write(response.read())

with open("temp.json", "r", encoding="UTF-8") as f:
    weather = json.loads(f.read())

#print(json.dumps(weather, indent=" "))


city_weather = [(w['id'],
                 w['name'],
                 dt.fromtimestamp(w['dt']).isoformat(sep=" "),
                 int(w['main']['temp']),
                 ",".join([str(img['id']) for img in w['weather']])
                 ) for w in weather['list']]

#print(city_weather)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.executemany("INSERT INTO weather VALUES (?,?,?,?,?)", city_weather)
conn.commit()