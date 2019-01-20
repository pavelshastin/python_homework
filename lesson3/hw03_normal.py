# Задание-1:
# Напишите функцию, возвращающую ряд Фибоначчи с n-элемента до m-элемента.
# Первыми элементами ряда считать цифры 1 1

# n, m = list(map(int, input("Введите начало и конец участка последовательности Фибоначчи через пробел: ").split()))
#
# def fibonacci(n, m):
#     if n <= 0 or m <= 0:
#         return "Не верно введены границы участка"
#
#     numbers = ()
#
#     a = 1
#     b = 1
#
#     for i in range(m):
#
#         if i >= n - 1:
#             numbers += a,
#
#         a, b = b, a + b
#
#     return numbers
#
# print(fibonacci(n, m))


# Задача-2:
# Напишите функцию, сортирующую принимаемый список по возрастанию.
# Для сортировки используйте любой алгоритм (например пузырьковый).
# Для решения данной задачи нельзя использовать встроенную функцию и метод sort()


# def sort_to_max(*args):
#     if len(args) != 1:
#         return "The {} requires one argument. {} given".format("sort_to_max", len(args))
#     if type(args[0]).__name__ != "list":
#         return "The given argument is not a list"
#
#     flag = 0
#     i = 0
#     n = 0 # Number of outer iterations
#
#     while i < len(args[0]) - 1:
#
#         if args[0][i] > args[0][i+1]:
#             buf = args[0][i+1]
#             args[0][i+1] = args[0][i]
#             args[0][i] = buf
#             flag = 1
#
#         i += 1
#
#         if i == len(args[0]) - n - 1 and flag == 1:
#             print(i)
#             flag = 0
#             i = 0
#             n += 1
#
#     return args[0]
#
#
# print(sort_to_max([2, 10, -12, 2.5, 20, -11, 4, 4, 0]))


# Задача-3:
# Напишите собственную реализацию стандартной функции filter.
# Разумеется, внутри нельзя использовать саму функцию filter.

# def my_filter(*args):
#     if len(args) != 2:
#         return "Function requires 2 argument. {} given".format(len(args))
#     if hasattr(args[1], "__iter__") == False:
#         return "Not iterable object as second argument is given"
#     if type(args[0]).__name__ != 'function':
#         return "Not function as first argument is given"
#
#     init = args[1]
#     initType = type(init).__name__
#     func = args[0]
#     filtered = []
#
#     if initType != 'dict':
#         for el in init:
#             if func(el):
#                 filtered.append(el)
#
#     if initType == 'dict':
#         for el in init.keys():
#             if func(el):
#                 filtered.append(el)
#
#     return filtered
#
# print(my_filter(lambda x: x%2 == 0 , (1,2,3,4,5)))
# print(my_filter(lambda x: type(x).__name__ != "str" , {"one": 1, "two": 2}))




# Задача-4:
# Даны четыре точки А1(х1, у1), А2(x2 ,у2), А3(x3 , у3), А4(х4, у4).
# Определить, будут ли они вершинами параллелограмма.
import math
# inputStr = "3,5 7,12 12,9 8,2"

a1, a2, a3, a4 = list(map(lambda x: tuple(map(int, x.split(","))), list(map(str, inputStr.split()))))


def isParallelogram(a1, a2, a3, a4):
    """
    Compares opposite edges of 4-points perimeter. If they are equal than returns true, otherwise false
    :param a1: tuple (x,y)
    :param a2: tuple (x,y)
    :param a3: tuple (x,y)
    :param a4: tuple (x,y)
    :return: bool
    """

    coords = sorted([a1, a2, a3, a4])

    edge12 = math.sqrt((coords[1][0] - coords[0][0])**2 + (coords[1][1] - coords[0][1])**2)
    edge13 = math.sqrt((coords[2][0] - coords[0][0])**2 + (coords[2][1] - coords[0][1])**2)
    edge24 = math.sqrt((coords[3][0] - coords[1][0])**2 + (coords[3][1] - coords[1][1])**2)
    edge34 = math.sqrt((coords[3][0] - coords[2][0])**2 + (coords[3][1] - coords[2][1])**2)


    if edge12 == edge34 and edge13 == edge24:
        return True

    return False


print(isParallelogram(a1, a2, a3, a4))