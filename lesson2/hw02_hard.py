__author__ = 'Шастин Павел'

# Задание-1: уравнение прямой вида y = kx + b задано в виде строки.
# Определить координату y точки с заданной координатой x.

equation = 'y = -12x + 11111140.2121'
x = 2.5
# вычислите и выведите y


# Задание-2: Дата задана в виде строки формата 'dd.mm.yyyy'.
# Проверить, корректно ли введена дата.
# Условия корректности:
# 1. День должен приводиться к целому числу в диапазоне от 1 до 30(31)
#  (в зависимости от месяца, февраль не учитываем)
# 2. Месяц должен приводиться к целому числу в диапазоне от 1 до 12
# 3. Год должен приводиться к целому положительному числу в диапазоне от 1 до 9999
# 4. Длина исходной строки для частей должна быть в соответствии с форматом 
#  (т.е. 2 символа для дня, 2 - для месяца, 4 - для года)

# Пример корректной даты
date = '01.11.1985'

# Примеры некорректных дат
date = '01.22.1001'
date = '1.12.1001'
date = '-2.10.3001'


# Задание-3: "Перевёрнутая башня" (Задача олимпиадного уровня)
#
# Вавилонцы решили построить удивительную башню —
# расширяющуюся к верху и содержащую бесконечное число этажей и комнат.
# Она устроена следующим образом — на первом этаже одна комната,
# затем идет два этажа, на каждом из которых по две комнаты, 
# затем идёт три этажа, на каждом из которых по три комнаты и так далее:
#         ...
#     12  13  14
#     9   10  11
#     6   7   8
#       4   5
#       2   3
#         1
#
# Эту башню решили оборудовать лифтом --- и вот задача:
# нужно научиться по номеру комнаты определять,
# на каком этаже она находится и какая она по счету слева на этом этаже.
#
# Входные данные: В первой строчке задан номер комнаты N, 1 ≤ N ≤ 2 000 000 000.
#
# Выходные данные:  Два целых числа — номер этажа и порядковый номер слева на этаже.
#
# Пример:
# Вход: 13
# Выход: 6 2
#
# Вход: 11
# Выход: 5 3

# Задача 1
import re

equation = input("Введите линейное уравнение в формате y = kx + b: ")
x = float(input("Введите аргумент x: "))

def LinearEquation(eq):
    def __check__(eq):
        return True if re.match(r"^[a-z]=[-+0-9]*\.{0,1}[0-9]*[a-z][0-9+-]*\.{0,1}[0-9]*$", eq.replace(" ", "")) else False

    def __parse__(eq):
        rightPart = re.split(r"=", eq.replace(" ", ""))[1]
        leftSplit = re.split(r"[a-z]", rightPart)

        if leftSplit[0]:
            k = float(leftSplit[0]) if leftSplit[0] != "-" else -1
        else:
            k = 1

        b = float(leftSplit[1]) if leftSplit[1] else 0
        return {"k": k, "b": b}

    def __solve__(var):
        facts = __parse__(eq)
        y = facts["k"]*float(var) + facts["b"]
        return y

    def __error__(var):
        return "Уравнение не соответсвует шаблону y = kx + k"

    if __check__(eq):
        return __solve__

    return __error__

linearEquation = LinearEquation(equation)
print(linearEquation(x))

# Задача 2

initDate = input("Введите дату: ")

def checkDate(date):
    format = "dD/MM/Yyyy".lower()

    dateFormat = {
        "month_day": {1: 31, 2: 28, 3: 31, 4: 30, 5: 30, 6: 31, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31},
        "yearMax": {1: 2, 2: 2, 3: 4, 4: 4}[format.count("y")] or 4,  #Подгоняет указанные формат года под возможный
        "monthMax": {1: 1, 2: 2}[format.count("m")] or 2,
        "dayMax": {1: 1, 2: 2}[format.count("d")] or 2,
        "delimeter": {0: "/", 2: "."}[format.count(".") or 0]
    }

    #print(dateFormat["yearMax"])

    if len(date) > (dateFormat["yearMax"] + dateFormat["monthMax"] + dateFormat["dayMax"] + 2):
        return "Количество символов в дате больше указанного формата"

    delimeter = dateFormat["delimeter"]
    if date.count(delimeter) !=2:
        return "Указан не верный разделитель \"{}\" или количесво разделителей не равно 2".format(delimeter)

    day, month, year = initDate.split(delimeter)
    dayInt, monthInt, yearInt = list(map(int, initDate.split(delimeter)))


    errorMessage = ""

    if len(day) != dateFormat["dayMax"]:
        errorMessage += "Количество символов дня в дате не соответсвует заданному формату\n"
    if len(month) != dateFormat["monthMax"]:
        errorMessage += "Количество символов месяца в дате не соответсвует заданному формату\n"
    if len(year) != dateFormat["yearMax"]:
        errorMessage += "Количество символов года в дате не соответсвует заданному формату\n"
    if dayInt < 1:
        errorMessage += "День не может быть отрицательным числом или нулем\n"
    if monthInt < 1:
        errorMessage += "Месяц не может быть отрицательным числом или нулем\n"
    if yearInt < 1:
        errorMessage += "Год не может быть отрицательным числом или нулем\n"
    if  0 < monthInt > 31:
        errorMessage += "Номер дня не может быть больше 31\n"
    if 0 < monthInt > 12:
        errorMessage += "Номер месяца не может быть больше 12\n"
    if 0 < monthInt <= 12 and 0 < dayInt > dateFormat["month_day"][monthInt]:
        errorMessage += "Количество дней в данном месяце меньше\n"

    if errorMessage:
        return errorMessage
    else:
        return "Дата соответсвует формату"


print(checkDate(initDate))



#Задача 3

roomNum = int(input("Введите номер комнаты: "))

floor = 2
room = 2
block = 2
stop = False

while True:
    if roomNum == 1:
        print(1, 1)
        break

    for _ in range(block):
        for numLeft in range(block):
            #print(block, floor, room)

            if room == roomNum:
                print(floor, numLeft + 1)
                stop = True
                break
            room += 1

        if stop:
            break
        floor += 1

    if stop:
        break
    block += 1




