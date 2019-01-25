# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки они получают
# удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла

import os
import re

class DataBase:
    """

    """
    def __init__(self, db_name):
        cur_dir = os.getcwd()

        if cur_dir.split("\\")[-1:][0] != db_name:
            if os.path.exists(db_name):
                os.chdir(db_name)
            else:
                raise FileNotFoundError("Database doesn't exist")

        self.db_name = db_name
        self.headers = {}
        self.f = None
        self.table = None


    def connect(self, table):
        if self.f is None:
            self.f = open(table, "r", encoding="UTF-8")
            self.table = table
            return self
        raise ValueError("To establish new connection you need to close previous one.")

    def getHeaders(self):
        if self.headers[self.table] is None:
            self.f.__iter__()
            line = self.f.readline()

            self.headers[self.table] = tuple(map(lambda x: x.strip(), re.split(r" {3,}", line)))

        return self.headers[self.table]

    def getAll(self):
        self.f.__iter__()
        headers = self.getHeaders()
        return list(map(lambda line: dict(zip(headers, line.split())), self.f.readlines()))

    def nextLine(self):
        pass

    def close(self):
        self.f.close()
        self.f = None



db = DataBase("data")

print(os.getcwd())
print(db.connect("hours_of").getAll())
db.close()
print(db.connect("workers").getAll())

