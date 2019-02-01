#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87      
      16 49    55 77    88    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""

import random


class Cell:
    def __init__(self):
        pass


class Card:
    def __init__(self):
        self.card_columns = [list(range(1, 10))] + [list(range(i, i + 10)) for i in range(10, 79, 10)] + [list(range(80, 91))]

        rounds = 0
        while True:
            rounds += 1
            card_list = self.create_rand_list(1, 90, 15)

            if self.__check_rand_list(card_list):
                self.card_list = card_list
                break

        #print(rounds, self.card_list)
        self.card_mtx = self.__create_mtx()


    @staticmethod
    def create_rand_list(start, end, num):
        seq = list(range(start, end))
        rand_int = random.randint(0, len(seq)-1)

        if rand_int + num > len(seq) - 1:
            rand_int = len(seq) - num

        random.shuffle(seq)
        return sorted(seq[rand_int:rand_int + num])


    def __check_rand_list(self, rand_list):

        for col in self.card_columns:
            q = 0
            for num in rand_list:
                if num in col:
                    #print(num, q, col)
                    q += 1
                if q > 3:
                    return False
        return True


    def __create_mtx(self):
        #zero-matrix
        mtx = dict(enumerate([dict(enumerate([0]*9)), dict(enumerate([0]*9)), dict(enumerate([0]*9))]))

        #enumerated card columns
        card_columns = dict(enumerate(self.card_columns))

        #row-numerated matrix of random values
        nums_mtx = dict(enumerate([self.card_list[0::3], self.card_list[1::3], self.card_list[2::3]]))

        #Positioning random values to appropriate cells of card (zero-matrix)
        for row in nums_mtx:
            for num in nums_mtx[row]:
                for col in card_columns:
                    if num in card_columns[col]:

                        mtx[row][col] = num
                        break

        print(mtx)




    @property
    def numbers(self):
        return self.card_list


comp_card = Card()
print(comp_card.numbers)