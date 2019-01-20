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


def sort_to_max(origin_list):
    pass

sort_to_max([2, 10, -12, 2.5, 20, -11, 4, 4, 0])






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