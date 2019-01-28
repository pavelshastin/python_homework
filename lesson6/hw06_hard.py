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
init_db_dir = os.getcwd()

class DataBase:

    def __init__(self, db_name):
        cur_dir = os.getcwd()

        if cur_dir.split("\\")[-1:][0] != db_name:
            if os.path.exists(db_name):
                os.chdir(db_name)
            else:
                raise FileNotFoundError("Database doesn't exist")

        self.db_name = db_name
        self.headers = None
        self.f = None
        self.head_line = False



    def connect(self, table):
        if self.f is None:
            self.f = open(table, "r", encoding="UTF-8")
            self._setHeaders(self.f)
            return self

        if self.f.name == table:
            return self

        raise ValueError("To establish new connection you need to close previous one.")

    def _setHeaders(self, f_iter):
        if self.headers is None:
            f_iter.seek(0, 0)
            line = f_iter.readline()

            self.headers = tuple(map(lambda x: x.strip(), re.split(r" {3,}", line)))


    def getHeaders(self):
        return self.headers if self.headers else None


    def getAll(self):
        self.f.seek(0, 0)
        self.f.readline() #to skip the first header line

        res = list(map(lambda line: dict(zip(self.headers, line.split())), self.f.readlines()))

        self.f.seek(0, 0) #to return the caret to the beginning

        return res

    def close(self):
        self.f.close()
        self.f = None
        self.headers = None


    def __iter__(self):
        self.f.seek(0, 0)
        self.f.readline()  # to skip the first header line

        if self.headers is None:
            self.getHeaders()

        for line in self.f:
            yield dict(zip(self.headers, line.split()))

        self.f.seek(0, 0)
        self.head_line = False


    def __next__(self):
        #to skip the first header line
        if self.head_line is False:
            self.f.readline()
            self.head_line = True
        res = dict(zip(self.headers, self.f.readline().split()))

        return res if res else False


db = DataBase("data")


print(db.connect("hours_of").getAll())
db.close()
print(db.connect("workers").getHeaders())
print(db.connect("workers").getAll())

