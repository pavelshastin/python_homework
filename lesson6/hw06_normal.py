#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Задание-1:
# Реализуйте описаную ниже задачу, используя парадигмы ООП:
# В школе есть Классы(5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя(мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать 
# в неограниченном кол-ве классов свой определенный предмет. 
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.

# Выбранная и заполненная данными структура должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов указанного ученика 
#  (Ученик --> Класс --> Учителя --> Предметы)
# 4. Узнать ФИО родителей указанного ученика
# 5. Получить список всех Учителей, преподающих в указанном классе
import re
import random

"""
    CREATING INITIAL DATA AND DIVIDING IT INTO GROUPS: PEOPLE, CLASSES, TEACHERS, PARENTS
"""

rand_people = list(re.split(r"\s{2,}", """
    Казаков Лавр Артемович
    Щукин Виталий Тарасович
    Чернов Григорий Проклович
    Пестов Тарас Макарович
    Блинов Василий Давидович
    Уваров Дональд Геласьевич
    Гаврилов Дмитрий Егорович
    Пономарёв Аполлон Наумович
    Кириллов Аверьян Рудольфович
    Брагин Гордей Авдеевич
    Щукин Алексей Улебович
    Орехов Руслан Павлович
    Дорофеев Вениамин Яковлевич
    Стрелков Ибрагил Еремеевич
    Моисеев Владислав Авксентьевич
    Кошелев Болеслав Германнович
    Медведев Кондрат Мартынович
    Харитонов Виталий Платонович
    Филатов Глеб Арсеньевич
    Пономарёв Орест Леонидович
    Лаврентьев Корнелий Куприянович
    Доронин Лазарь Олегович
    Громов Вениамин Фролович
    Макаров Адриан Ильяович
    Наумов Петр Мэлсович
    Уваров Вениамин Глебович
    Фёдоров Клим Федотович
    Сидоров Виссарион Егорович
    Меркушев Зиновий Константинович
    Кабанов Геннадий Мэлсович
    Зимин Евгений Филатович
    Шарапов Адриан Романович
    Фокин Любомир Демьянович
    Моисеев Оскар Михаилович
    Агафонов Назарий Глебович
    Игнатов Вячеслав Филатович
    Шестаков Лука Валерьянович
    Кудрявцев Станислав Богданович
    Голубев Аристарх Николаевич
    Наумов Юлиан Феликсович
    Орлов Исаак Валерьянович
    Сидоров Казимир Яковлевич
    Ларионов Аверьян Григорьевич
    Муравьёв Игнат Евгеньевич
    Корнилов Вениамин Георгьевич
    Молчанов Авраам Лаврентьевич
    Михайлов Соломон Максимович
    Доронин Валентин Мартынович
    Нестеров Эрик Геласьевич
    Егоров Ипполит Львович
    Трофимов Егор Оскарович
    Игнатов Владлен Семёнович
    Васильев Игнат Альвианович
    Наумов Ермак Парфеньевич
    Гусев Мстислав Степанович
    Наумов Ефрем Мэлорович
    Макаров Анатолий Олегович
    Воронцов Пантелей Сергеевич
    Дроздов Клемент Никитевич
    Лапин Эрик Адольфович
    Степанов Виталий Иринеевич
    Осипов Аскольд Викторович
    Мельников Родион Авксентьевич
    Матвеев Леонтий Натанович
    Корнилов Климент Всеволодович
    Королёв Исак Улебович
    Брагин Арнольд Кимович
    Чернов Архип Онисимович
    Суханов Руслан Андреевич
    Гущин Кондратий Александрович
    Маслов Федор Ильяович
    Муравьёв Родион Глебович
    Владимиров Адольф Святославович
    Кабанов Глеб Павлович
    Уваров Кондрат Федосеевич
    Щукин Юлий Улебович
    Коновалов Соломон Иванович
    Суворов Аристарх Геласьевич
    Силин Леонтий Павлович
    Давыдов Мирон Владленович
    Анисимов Ефрем Олегович
    Воронцов Пантелей Альбертович
    Якушев Василий Юлианович
    Корнилов Гавриил Альбертович
    Соловьёв Арнольд Аристархович
    Морозов Август Даниилович
    Чернов Никифор Артемович
    Сергеев Гаянэ Гордеевич
    Комиссаров Мстислав Федосеевич
    Павлов Никифор Юрьевич
    Соболев Любовь Аркадьевич
    Морозов Адриан Павлович
    Григорьев Владислав Ярославович
    Сергеев Родион Максович
    Тетерин Михаил Якунович
    Русаков Илья Федотович
    Галкин Гаянэ Станиславович
    Быков Илларион Степанович
    Громов Владислав Аркадьевич
    Кулаков Рубен Олегович
    Самойлов Людвиг Эльдарович
    Прохоров Ефрем Робертович
    Баранов Арсен Тарасович
    Кузнецов Май Романович
    Лукин Исаак Давидович
    Прохоров Олег Ильяович
    Александров Оскар Адольфович
    Беляков Панкратий Валерьянович
    Воронцов Гаянэ Львович
    Брагин Панкрат Борисович
    Мухин Лукьян Ефимович
    Колесников Илларион Фролович
    Смирнов Рудольф Гордеевич
    Голубев Адам Оскарович
    Котов Эрик Тимофеевич
    Рябов Мартин Михаилович
    Кудрявцев Пантелей Мартынович
    Зиновьев Вальтер Вениаминович
    Кондратьев Егор Петрович
    Константинов Арнольд Миронович
    Селиверстов Мирон Тимофеевич
    Уваров Бенедикт Фролович
    Воробьёв Любомир Проклович
    Миронов Максим Александрович
    Алексеев Евгений Львович
    Иванов Игнатий Натанович
    Гордеев Алексей Кимович
    Смирнов Арсений Лукьевич
    Рогов Абрам Куприянович
    Лебедев Яков Юрьевич
    Артемьев Игнат Даниилович
    Русаков Марк Антонович
    Корнилов Пантелеймон Германович
    Артемьев Антон Викторович
    Шаров Венедикт Анатольевич
    Федосеев Мечеслав Наумович
    Пахомов Корнелий Николаевич
    Воробьёв Адольф Станиславович
    Мамонтов Владислав Семёнович
    Гущин Афанасий Ильяович
    Зиновьев Никифор Сергеевич
    Журавлёв Пантелей Владленович
    Данилов Вольдемар Валерьевич
    Новиков Людвиг Валерьянович
    Некрасов Геннадий Евсеевич
    Котов Эрнест Игнатьевич
    Муравьёв Игнатий Вячеславович
    Лобанов Илларион Тарасович
    Сафонов Яков Платонович
    Михайлов Максимилиан Эльдарович
    Зыков Валентин Евсеевич
    Субботин Абрам Еремеевич
    Рогов Вальтер Робертович
    Одинцов Харитон Георгьевич
    Дорофеев Моисей Митрофанович
    Кудрявцев Зиновий Святославович
    Моисеев Денис Давидович
    Селезнёв Аввакуум Евсеевич
    Трофимов Севастьян Платонович
    Белоусов Прохор Германнович
    Бобылёв Наум Улебович
    Потапов Виталий Еремеевич
    Медведев Венедикт Наумович
    Панов Устин Максимович
    Кабанов Бенедикт Никитевич
    Евдокимов Вольдемар Парфеньевич
    Лазарев Василий Кириллович
    Нестеров Архип Викторович
    Козлов Вальтер Леонидович
    Бобылёв Гордей Ефимович
    Тимофеев Вячеслав Алексеевич
    Крылов Гавриил Еремеевич
    Громов Аскольд Степанович
    Кабанов Нисон Витальевич
    Казаков Аверьян Макарович
    Лыткин Севастьян Донатович
""".strip()))


rand_people = list(map(lambda x: dict(zip(["surname", "name", "patriotic"], x.split())), rand_people))

#print(len(rand_people), rand_people)

#-----------------------
subjects = ["русский язык", "литература", "математика", "физика", "информатика", "биология", "география", \
            "английский язык", "астрономия", "химия"]


people = dict(enumerate(rand_people))

classes = {"5А": {"subjects": {}, "pupils": []}, "7Б": {"subjects": {}, "pupils": []}, \
           "3В": {"subjects": {}, "pupils": []}, "8Г": {"subjects": {}, "pupils": []}}
parents = {}
teachers = {}
#--------------------------


#list of people ids
p_range = list(range(0, len(people)-1))

#20 teachers for 10 subjects
i = 0
for _ in range(20):
    r = random.choice(p_range)
    p_range.remove(r) #excluding chosen elements

    if r not in teachers.keys():
        teachers[r] = {"subject": subjects[i], "classes": []}

    i += 1
    i = 0 if i == len(subjects) else i #we have more teachers than subjects


#subjects for classes

subj_whole = dict(enumerate(subjects * round(len(classes)*5/len(subjects)))) #each class has 5 subjects to learn. 20 choices for 10 subjects
subj_range = list(range(len(subj_whole)))
q_subj = len(subj_whole)


while q_subj > 0:
    for cl_id, cl in classes.items():
        if len(subj_range) == 0:
            break

        r = random.choice(subj_range)


        if subj_whole[r] in cl["subjects"]:
            continue

        subj_range.remove(r)
        cl["subjects"][subj_whole[r]] = ""
        q_subj -= 1

        if q_subj == 0:
           break



#Quantity of pupils and parents: 1.5 parents per pupil
q_pupils = round((len(people) - len(teachers))/(1.5 + 1))
q_parents = len(people) - len(teachers) - q_pupils


#Choosing pupils and separating them into classes
while q_pupils > 0:
    for cl in classes.keys():
        r = random.choice(p_range)
        p_range.remove(r)  #excluding chosen elements

        classes[cl]["pupils"].append(r)

        q_pupils -= 1
        if q_pupils == 0 or len(p_range) == 0:
            break

#Choosing parents for every pupil in class

while q_parents > 0:
    #print(q_parents)
    for cl, pupils in classes.items():

        for p in pupils["pupils"]:
            if len(p_range) == 0:
                break

            r = random.choice(p_range)
            p_range.remove(r)  # excluding chosen elements

            if p not in parents.keys():
                parents[p] = [r]
            else:
                parents[p].append(r)

            q_parents -= 1
            if q_parents == 0:
                print(p_range)
                break

    if q_parents == 0 or len(p_range) == 0:
        break


#Assining teachers for classes

for cl_id, cl in classes.items():
    for s in cl["subjects"].keys():
        teach = {}

        #Searching for all teachers of subject <s>
        for t_id, t in teachers.items():
            if t["subject"] == s:
                teach[t_id] = len(t["classes"])

        #A teacher with minimal current classes to teach
        min_teach = min(teach, key=teach.get)

        #Assigning a new class to that teacher
        cl["subjects"][s] = min_teach
        teachers[min_teach]["classes"].append(cl_id)



#print(people)
#print(len(teachers), teachers)
#print(classes)
#print(len(parents), parents)





class PersonNotFound(Exception):
    def __init__(self, type, surname, name, patriotic):
        """
        An Exception thrown when a person is not found in DB
        :param type: str
        :param surname: str
        :param name: str
        :param patriotic: str
        """
        self.surname = surname.title()
        self.name = name.title()
        self.patriotic = patriotic.title()
        self.type = type.title()
        self.dbs = {"Person": "People", "Pupil": "Pupils", "Teacher": "Teachers", "Parent": "Parents"}

    def __str__(self):
        return "{} {} {} {} not found among {}".format(self.type, self.surname, self.name, self.patriotic, self.dbs[self.type])




class Person:

    #Checking if the person exists in DB by his id
    def __new__(cls, surname, name, patriotic):
        per_id = None

        for id, person in people.items():
            if person["surname"] == surname and person["name"] == name and person["patriotic"] == patriotic:
                per_id = id


        if per_id == None:
            raise PersonNotFound("Person", surname, name, patriotic)

        instance = super(Person, cls).__new__(cls)

        instance.per_id = per_id

        return instance


    def __init__(self, surname, name, patriotic):

        self.name = name.strip().title()
        self.surname = surname.strip().title()
        self.patriotic = patriotic.strip().title()


    def get_id(self):
        return self.per_id

    @property
    def full_name(self):
        return "{} {} {}".format(self.surname, self.name, self.patriotic)

    @property
    def short_name(self):
        return "{} {}.{}.".format(self.surname, self.name[:1], self.patriotic[:1])




class Pupil(Person):
    # Checking if the pupil with given name exists in CLASSES by it's id
    def __new__(cls, surname, name, patriotic):

        instance = super(Pupil, cls).__new__(cls, surname, name, patriotic)

        per_id = instance.per_id


        cl_id = list(filter(lambda cl: per_id in list(classes[cl]["pupils"]), classes))

        if len(cl_id) == 0:
            raise PersonNotFound("Pupil", surname, name, patriotic)

        instance.__cl_id = cl_id[0]
        return instance



    def __init__(self, surname, name, patriotic):
        self.surname = surname
        self.name = name
        self.patriotic = patriotic

    @property
    def class_id(self):
        return self.__cl_id

    @property
    def subjects(self):
        self.subjects = classes[self.__cl_id]["subjects"]

        return list(classes[self.__cl_id]["subjects"].keys())

    @property
    def parents(self):
        p_parents = [people[p_id] for p_id in parents[self.per_id]]
        self.__parents_list = [Person(p["surname"], p["name"], p["patriotic"]) for p in p_parents]
        return self.__parents_list

    @property
    def pupil_card(self):
        return {
            "surname": self.surname,
            "name": self.name,
            "patritic": self.patriotic,
            "class": self.__cl_id,
            "parents": self.get_parents()
        }



class Teacher(Person):
    # Checking if the teacher with given name exists in TEACHERS by his id
    def __new__(cls, surname, name, patriotic):
        instance = super(Teacher, cls).__new__(cls, surname, name, patriotic)

        per_id = instance.per_id

        if per_id not in teachers.keys():
            raise PersonNotFound("Teacher", surname, name, patriotic)

        instance.__classes = teachers[per_id]["classes"]
        instance.__subject = teachers[per_id]["subject"]
        return instance

    def __init__(self, surname, name, patriotic):
        self.surname = surname
        self.name = name
        self.patriotic = patriotic

    @property
    def subject(self):
        return self.__subject

    @property
    def classes(self):
        return self.__classes




class SchoolClass:
    def __init__(self, cl_id):
        """
        Initializing SchoolClass object. Recieving data about subjects which are taught in class,
        pupils that learn in class. Creating a list on Pupil onjects
        :param cl_id: str
        """
        self.__cl_id = cl_id
        self.subjects_list = classes[cl_id]["subjects"]
        self.pupil_ids = classes[cl_id]["pupils"]

        self.pupils_list = []
        for pl_id in self.pupil_ids:
            p = people[pl_id]

            self.pupils_list.append(Pupil(p["surname"], p["name"], p["patriotic"]))

    @property
    def class_id(self):
        return self.__cl_id

    @property
    def subjects(self):
        if self.subjects_list is None:
            self.subjects_list = classes[self.__cl_id]["subjects"]

        return list(self.subjects_list.keys())

    @property
    def teachers(self):
        if self.subjects_list is None:
            self.subjects_list = classes[self.__cl_id]["subjects"]

        self.teachers_list = []
        for s, t_id in self.subjects_list.items():
            p = people[t_id]
            self.teachers_list.append(Teacher(p["surname"], p["name"], p["patriotic"]))

        return self.teachers_list

    @property
    def pupils(self):
        return self.pupils_list

    def add_pupil(self, surname, name, patriotic):
        pass





class School:
    def __init__(self):
        self.classes = []
        for cl_id in classes.keys():
            self.classes.append(SchoolClass(cl_id))
        #caching data
        self.pupils = []
        self.parents = []

    def get_all_classes(self):
        return [cl.class_id for cl in self.classes]


    def get_all_pupils_of_cl(self, cl_id):
        cl = self.get_class_by_id(cl_id)
        return cl.pupils


    def get_pupil(self, surname, name, patriotic):
        return Pupil(surname, name, patriotic)


    def get_class_by_id(self, cl_id):
        cl_id = cl_id.strip().upper().replace(" ", "")

        return [cl for cl in self.classes if cl.class_id == cl_id][0]

    def get_all_pupils(self):
        pass

    def rename_class(self, cl_id, new_cl_id):
        pass




school = School()

pupils_5A = school.get_all_pupils_of_cl("5 а")

pupil = pupils_5A[0]
surname, name, patriotic = pupil.full_name.split()

#print(pupil.class_id, surname, name, patriotic)

pupil_1 = school.get_pupil(surname, name, patriotic)

parents = [p.full_name for p in pupil_1.parents]

class_pupil_1 = SchoolClass(pupil_1.class_id)

class_subjects = class_pupil_1.subjects

class_teachers = [{t.subject: t.full_name} for t in class_pupil_1.teachers]


print("List of all classes in the school: ", school.get_all_classes())
print("pupils of 5A class: ", [pl.full_name for pl in pupils_5A])
print("pupil: ", pupil_1.full_name)
print("parents: ", parents)
print("class: ", class_pupil_1.class_id)
print("subjects: ", class_subjects)
print("teachers: ", class_teachers)