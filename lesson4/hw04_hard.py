# Задание-1:
# Матрицы в питоне реализуются в виде вложенных списков:
# Пример. Дано:
matrix = [[1, 0, 8],
          [3, 4, 1],
          [0, 4, 2]]


# Выполнить поворот (транспонирование) матрицы
# Пример. Результат:
# matrix_rotate = [[1, 3, 0],
#                  [0, 4, 4],
#                  [8, 1, 2]]

# Суть сложности hard: Решите задачу в одну строку

transMatrix = list(map(list, zip(*matrix)))
print(transMatrix)


# Задание-2:
# Найдите наибольшее произведение пяти последовательных цифр в 1000-значном числе.
# Выведите произведение и индекс смещения первого числа последовательных 5-ти цифр.
# Пример 1000-значного числа:
number = """
17653731671330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450"""


number = number.replace("\n", "")

firsts = list(map(int, number[0::5]))
seconds = list(map(int, number[1::5]))
thirds = list(map(int, number[2::5]))
forths = list(map(int, number[3::5]))
fifths = list(map(int, number[4::5]))


num_matrix = list(map(list, (zip(firsts, seconds, thirds, forths, fifths))))

def prod_list(*args):
    if len(args) != 1:
        return "The function requieres 1 argument. {} given".format(len(args))
    if type(args[0]).__name__ != "list":
        return "The given argument is not a list"
    prod = 1

    for i in args[0]:
        prod *= i

    return prod


prods = list(map(prod_list, num_matrix))
max_prod = max(prods)
max_idx = prods.index(max_prod)*5

print(num_matrix)
print(max_prod, max_idx)



# Задание-3 (Ферзи):
# Известно, что на доске 8×8 можно расставить 8 ферзей так, чтобы они не били
# друг друга. Вам дана расстановка 8 ферзей на доске.
# Определите, есть ли среди них пара бьющих друг друга.
# Программа получает на вход восемь пар чисел,
# каждое число от 1 до 8 — координаты 8 ферзей.
# Если ферзи не бьют друг друга, выведите слово NO, иначе выведите YES.

import re


inputStr = input("Введите координаты ферзей в формате (x,y) через пробел: ")
#inputStr = "(1,2) (2,4) (3,6) (4,8) (5,3) (6,1) (7,7) (8,5)"
q_coords = list(map(lambda x: tuple(map(lambda y: int(y)-1, re.findall(r"\d", x))), inputStr.split()))

print("Matrix coords: ", q_coords)

def queens_fight(q_coords):
    matrix = [[0 for _ in range(8)] for _ in range(8)]
    ind_coords = {}

    #Creating a lists of the queen fighting coordinates
    for q in q_coords:
        ind_coords[q] = [q]

        # Horizontal and vertiacal coordinates
        for i, line in enumerate(matrix):
            for j, el in enumerate(line):
                if i == q[0] or j == q[1]:
                    ind_coords[q].append((i, j))

        # Diagonal coordinates
        i = q[0]
        j = q[1]

        while i < 7 and j < 7:
            i += 1
            j += 1
            #print("1: ", i, j)
            ind_coords[q].append((i, j))

        i = q[0]
        j = q[1]

        while i > 0 and j > 0:
            i -= 1
            j -= 1
            #print("2: ", i, j)
            ind_coords[q].append((i, j))

        i = q[0]
        j = q[1]

        while i < 7 and j > 0:
            i += 1
            j -= 1
            #print("3: ", i, j)
            ind_coords[q].append((i, j))

        i = q[0]
        j = q[1]

        while i > 0 and j < 7:
            i -= 1
            j += 1
            #print("4: ", i, j)
            ind_coords[q].append((i, j))

    #checking coordinates
    for q in q_coords:
        for key, coords in ind_coords.items():
            if key == q:
                continue

            if q in coords:
                return "YES"

    return "NO"

print(queens_fight(q_coords))