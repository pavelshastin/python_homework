
""" OpenWeatherMap (экспорт)

Сделать скрипт, экспортирующий данные из базы данных погоды, 
созданной скриптом openweather.py. Экспорт происходит в формате CSV или JSON.

Скрипт запускается из командной строки и получает на входе:
    export_openweather.py --csv filename [<город>]
    export_openweather.py --json filename [<город>]
    export_openweather.py --html filename [<город>]
    
При выгрузке в html можно по коду погоды (weather.id) подтянуть 
соответствующие картинки отсюда:  http://openweathermap.org/weather-conditions

Экспорт происходит в файл filename.

Опционально можно задать в командной строке город. В этом случае 
экспортируются только данные по указанному городу. Если города нет в базе -
выводится соответствующее сообщение.

"""

import csv
import json
import sys
import json
import csv
import os
import sqlite3 as db

if len(sys.argv[1:]) != 3:
    print("The export command requires 3 arguments <--format> <filename> <city>")
    print("If your city name has more than one word put it in quotes like 'New York'")
    quit()


if sys.argv[1][:2] != "--":
    print("The format command requires -- prefix")
    quit()

format = sys.argv[1][2:]
filename = sys.argv[2].lower()
cityname = sys.argv[3].title()
db_name = "weather.sqlite"
#print(format, filename, cityname)

export = ""

conn = db.connect(db_name)
cur = conn.cursor()

export = cur.execute("SELECT * FROM weather WHERE name = '{}'".format(cityname)).fetchall()

conn.close()

if len(export) == 0:
    print("There is no city of {} in database".format(cityname))
    quit()

print(export)

exp_struct = []
f_path = filename + "." + format

if format == "json":

    for city in export:
        id, name, date, t, w_ids = city

        exp_struct.append({
            "id": id,
            "name": name,
            "date": date,
            "t": t,
            "w_ids": tuple(w_ids.split(","))
        })

        dump = json.dumps(exp_struct, indent=4)


        with open(f_path, "w", encoding="UTF-8") as f:
            f.write(dump)




if format == "csv":
    with open(f_path, "w", encoding="windows-1251") as csvfile:
        csv.register_dialect('excel-semicolon', delimiter=';')

        writer = csv.writer(csvfile, dialect="excel-semicolon")
        writer.writerow(("id", "name", "date", "temp", "w_ids"))

        for city in export:
            id, name, date, temp, w_ids = city
            writer.writerow((id, name, date, temp, tuple(w_ids.split(","))))




if format == "html":
    div = """
        <div >
            <div>{id}</div>
            <div>{name}</div>
            <div>{date}</div>
            <div>
                <div>{temp}</div>
                <div>{imgs}></div>
            </div>
        </div>
    """

    divs = []

    for city in export:
        id, name, date, temp, icons = city

        icons = icons.split(";")

        imgs = []
        for i in icons:
            code = i.split(",")
            imgs.append("<img src='http://openweathermap.org/img/w/{}.png'/>".format(code[1].strip()))


        divs.append(div.format(id=id, name=name, date=date, temp=temp, imgs="".join(imgs)))

    html = "<html><body>{}</body></html>".format("".join(divs))

    with open(f_path, "w", encoding="utf-8") as htmlfile:
        htmlfile.write(html)


print("Weather data in {} loaded to {}".format(cityname, f_path))