# Задание-1:
# Написать программу, выполняющую операции (сложение и вычитание) с простыми дробями.
# Дроби вводятся и выводятся в формате:
# n x/y ,где n - целая часть, x - числитель, у - знаменатель.
# Дроби могут быть отрицательные и не иметь целой части, или иметь только целую часть.
# Примеры:
# Ввод: 5/6 + 4/7 (всё выражение вводится целиком в виде строки)
# Вывод: 1 17/42  (результат обязательно упростить и выделить целую часть)
# Ввод: -2/3 - -2
# Вывод: 1 1/3

# fractInput = input("Введите выражение сложения дробей в формате (-)n x/y -/+ (-)n x/y: ")
#
# def fractSplit(fract):
#     fract = fract.strip()
#     #Parsing data from fraction string to variables
#     try:
#         minusInd = fract.find("-", 1) #Со второго элемента, чтобы не захватить минус первой дроби
#         plusInd = fract.find("+", 1)
#
#         if minusInd != -1 and plusInd != -1:
#             if minusInd > plusInd:
#                 delimInd = plusInd
#                 delim = +1
#             else:
#                 delimInd = minusInd
#                 delim = -1
#         elif minusInd != -1 and plusInd == -1:
#             delimInd = minusInd
#             delim = -1
#         elif minusInd == -1 and plusInd != -1:
#             delimInd = plusInd
#             delim = +1
#
#         leftPart = fract[:delimInd].strip()
#         rightPart = fract[delimInd+1:].strip()
#
#         if len(leftPart.split()) > 1:
#             leftWhole, leftFract = leftPart.split()
#         else:
#             leftWhole = 0
#             leftFract = leftPart
#
#         if len(rightPart.split()) > 1:
#             rightWhole, rightFract = rightPart.split()
#         else:
#             rightWhole = 0
#             rightFract = rightPart
#
#
#         leftWhole = int(leftWhole)
#         leftNumer, leftDenom = list(map(int, leftFract.split("/")))
#
#         rightWhole = int(rightWhole)
#         rightNumer, rightDenom = list(map(int, rightFract.split("/")))
#
#         #Subtraction of given fractions
#
#         if leftWhole != 0:
#             leftNumer = leftWhole * leftDenom + (leftNumer if leftWhole > 0 else -leftNumer)
#         if rightWhole != 0:
#             rightNumer = rightWhole * rightDenom + (rightNumer if rightWhole > 0 else -rightNumer)
#
#         if rightDenom == leftDenom:
#             subNumer = leftNumer + rightNumer * delim
#             subDenom = rightDenom or leftDenom
#         else:
#             subNumer = leftNumer * rightDenom + rightNumer * leftDenom * delim
#             subDenom = rightDenom * leftDenom
#
#         resNumer = subNumer % subDenom
#         resWhole = int(subNumer/subDenom)
#         resDenom = subDenom
#
#         #If higher term fraction i.e. 2/4 or 3/6 or 2/6 or 13/169 or 88/1014
#
#         for i in range(2,9):
#             while resDenom % i == 0 and resNumer % i == 0:
#                 resDenom = resDenom/i
#                 resNumer = resNumer/i
#
#         if resDenom % resNumer == 0:
#             resDenom = resDenom/resNumer
#             resNumer = 1
#
#         #Format of return
#
#         if resNumer != 0 and resWhole != 0:
#              returnString = "{0} {1}/{2}"
#         elif resNumer == 0:
#              returnString = "{0}"
#         elif resWhole == 0:
#              returnString = "{1}/{2}"
#
#         return returnString.format(resWhole, int(resNumer), int(resDenom))
#
#     except ValueError:
#         return "Введенная дробь не соответсвует формату n x/y или указаны отличные или лишние знаки операции или пробелы."
#     except UnboundLocalError:
#         return "Введен нераспозноваемый набор символов"
#
# fraction = "5 12/1014 + 6 66/1014"
#
# print(fractSplit(fractInput))





# Задание-2:
# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки
# они получают удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# import os
#
# DIR = "data"
# workers = []
# hours_of = []
#
# with open(os.path.join(DIR, "workers"), "r", encoding="UTF-8") as ws:
#     ws.readline() # skipping first kine of file with column names
#
#     for line in ws:
#         worker = list(map(lambda x: int(x) if x.isnumeric() else x, line.split()))
#         if worker:
#             workers.append(worker)
#
#     #print(workers)
#
# with open(os.path.join(DIR, "hours_of"), "r", encoding="UTF-8") as hs:
#      hs.readline() # skipping first kine of file with column names
#
#      for line in hs:
#          hours = list(map(lambda x: int(x) if x.isnumeric() else x, line.split()))
#
#          if hours:
#             hours_of.append(hours)
#
#      #print(hours_of)
#
# #Merging "workers" and "hours_of" lists based on workers
# for hours in hours_of:
#
#     for worker in workers:
#         if hours[0] in worker and hours[1] in worker:
#             worker.append(hours[2])
#
# #Estimating salaries
# for worker in workers:
#     hoursNorm = worker[4]
#     salary = worker[2]
#     hoursWorked = worker[5]
#     hourRate = salary/hoursNorm
#
#     payment = hourRate * hoursWorked if hoursNorm > hoursWorked else salary + (hoursWorked - hoursNorm) * hourRate * 2
#     worker.append(round(payment, 2))
#
#
#
# #Justifing output
# tableHead = ['Имя', 'Фамилия', 'Зарплата', 'Должность', 'Норма_часов', 'Отработано_часов', 'Начислено']
# workers.insert(0, tableHead)
#
# workersTable = list(map(list, (zip(*workers))))
# workers = []
# for column in workersTable:
#     column = list(map(str, column))
#     maxLen = max(list(map(len, column)))
#
#     workers.append(list(map(lambda x: x.ljust(maxLen, " "), column)))
#
#
# workers = list(zip(*workers))
# print(workers)

#
# #Outputting the data to the salary file
#
# with open(os.path.join(DIR, "salary"), "a", encoding="UTF-8") as s:
#     for worker in workers:
#         s.write("   ".join(worker) + os.linesep)





# Задание-3:
# Дан файл ("data/fruits") со списком фруктов.
# Записать в новые файлы все фрукты, начинающиеся с определенной буквы.
# Т.е. в одном файле будут все фрукты на букву “А”, во втором на “Б” и т.д.
# Файлы назвать соответственно.
# Пример имен файлов: fruits_А, fruits_Б, fruits_В ….
# Важно! Обратите внимание, что нет фруктов, начинающихся с некоторых букв.
# Напишите универсальный код, который будет работать с любым списком фруктов
# и распределять по файлам в зависимости от первых букв, имеющихся в списке фруктов.
# Подсказка:
# Чтобы получить список больших букв русского алфавита:

import os

DIR = "data"

fruits = []
with open(os.path.join(DIR, "fruits.txt"), "r", encoding="UTF-8") as f:
    for line in f:
        if line.strip():
            fruits.append(line.strip())


if os.path.isdir(os.path.join(os.getcwd(), "fruits")) == False:
    os.mkdir(os.path.join(os.getcwd(), "fruits"))

letters = list(map(chr, range(ord('А'), ord('Я')+1)))
filteredList = []

# for l in letters:
#     l = l.title()
#
#     for fruit in fruits:





