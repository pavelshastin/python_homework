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
    """
    A cell is a lowerest-level object of the game. It has coordinates (col - column, row) and value (val)
    """

    def __init__(self, row, col, val):
        self.row_num = row
        self.col_num = col
        self.value = val

    @property
    def row(self):
        return self.row_num

    @property
    def col(self):
        return self.col_num

    @property
    def val(self):
        return self.value

    @row.setter
    def row(self, row):
        self.row_num = row

    @col.setter
    def col(self, col):
        self.col_num = col

    @val.setter
    def val(self, val):
        self.value = val


class Card:
    """
    Class creates a game card with 15 random DIFFERENT numbers divided into 3 rows of 5 elements. Each element is placed into\
    proper decimal column, For instance, 1 column - 1-9; 2 col - 10-19 ... 9 (last) col - 80-90.
    """

    def __init__(self):
        #Creates decimal columns
        self.card_columns = [list(range(1, 10))] + [list(range(i, i + 10)) for i in range(10, 79, 10)] + [list(range(80, 91))]

        #The cycle iterates through random bunches of numbers to choose the one that has only DIFFERENT random numbers
        rounds = 0
        while True:
            rounds += 1
            card_list = self.create_rand_list(1, 90, 15)

            if self.__check_rand_list(card_list):
                self.card_list = card_list
                break

        #print(rounds, self.card_list)
        self.cells = self.__create_cells()



    @staticmethod
    def create_rand_list(start, end, num):
        """
        Creates a SORTED list of random numbers in range(start, end) and quantity of num
        :param start: int
        :param end: int
        :param num: int
        :return:  sorted list
        """
        seq = list(range(start, end))

        #start number to make slice of random sequence
        rand_int = random.randint(0, len(seq)-1)

        #make sure that a sequence start number will cover a slice of 15 numbers, If it starts in 80 it will cover\
        #only 10 numbers. In this case we take last 15 numbers.
        if rand_int + num > len(seq) - 1:
            rand_int = len(seq) - num

        random.shuffle(seq)
        return sorted(seq[rand_int:rand_int + num])


    def __check_rand_list(self, rand_list):
        """
        Checks a list of random numbers in the way that guaranties existence of only 3 numbers of decimal grade.
        For instance, 50, 54, 56 - only 3, because each card has only 3 rows of particular decimal grade.
        The function checks if the given random number belongs to the particular card column. If the random list has
        more numbers than 3, the function returns False.
        :param rand_list: list
        :return: boolen
        """
        for col in self.card_columns:
            q = 0
            for num in rand_list:
                if num in col:
                    #print(num, q, col)
                    q += 1
                if q > 3:
                    return False
        return True


    def __create_cells(self):
        """
        The function creates/initializes 3*9 = 18 card card cells to be operated further in the game
        :return: list of Cell objects.
        """

        cells = []

        #enumerated card columns
        card_columns = dict(enumerate(self.card_columns))

        #Positioning random values to appropriate cells of card (zero-matrix)
        for row in range(3):
            #make a slice of 5 digits from a random 15-digits sorted list. Take slice of every third number.
            nums = self.card_list[row::3]

            for col in card_columns:
                brk = False

                for num in nums:
                    if num in card_columns[col]:
                        brk = True
                        cells.append(Cell(row, col, num))
                        break
                if brk:
                    continue

                #Cells that have no appropriate random numbers are filled with 0
                cells.append(Cell(row, col, 0))

        return cells



    def show_card(self):
        """
        THe function prints a game card row by row. It converts the 0-number cell value into "00" string and then is
        changed it into "  "- double space string to ensure that zeroes in such numbers as 20, 30 will not be changed.

        :return: nothing
        """

        for row in range(3):

            row_cells = list(filter(lambda c: c.row == row, self.cells))
            row_values = list(map(lambda c: " " + str(c.val) if len(str(c.val)) == 1 else str(c.val), row_cells)) #if one digit is given than add space before it
            row_strings = list(map(lambda v: "00" if v == " 0" else v, row_values)) # add 0 to single-zero-digit to prevent replacemant in numbers such 10, 20 etc

            res_str = "   ".join(row_strings)
            res_str = res_str.replace("00", "  ")
            res_str = res_str.replace(" X", "XX") #The sign shows that a player has covered the card cell with a drum.

            print(res_str)



class Player(Card):
    """
    Class creates a player that inherits methods from its parent
    """

    def __init__(self, name):
        Card.__init__(self)
        self.pl_name = name


    @property
    def name(self):
        return self.pl_name

    @name.setter
    def name(self, name):
        self.pl_name = name


    def check_card(self, num):
        """
        The function checks if the taken number from the drum bag (num) has the same number in the card. If no returns
        False. If Yes returns "one". If the card has any totally filled row it returns "all".
        :param num: int
        :return: boolean/str
        """
        check = False

        for c in self.cells:
            if c.val == num:

                c.val = "X"
                check = "one"
                break

        for i in range(3):
             full_row = []
             for c in self.cells:

                 if c.row == i and c.val == "X":

                     full_row.append(c)

             if len(full_row) == 5:
                 check = "all"
                 break


        return check




class DrumsBag:
    """
    Class creates a range(quant) of numbers (drums bag).
    """

    def __init__(self, quant):
        """

        :param quant: int
        """
        self.__bag = list(range(1, quant))


    def get_drum(self):
        """
        Returns a last number from randomly shuffled list that represents a drum.
        :return: int
        """
        if len(self.__bag) == 0:
            return None

        random.shuffle(self.__bag)

        return self.__bag.pop()



class Game(DrumsBag):
    """
    Iterating Class that represents a Game.
    """

    def __init__(self, *name):
        """
        Create a DrumBag and two players
        :param name: str
        """
        if len(name) != 1:
            raise TypeError("Require only one player. {} given".format(len(name)))


        if type(name[0]) is not str:
            raise TypeError(self.__name__ + ". Wrong type of arguments")

        DrumsBag.__init__(self, 90)

        self.player = Player(name[0])
        self.comp = Player("Компьютер")


    def __show_game(self):
        """
        Prints the game situation of a turn.
        :return: nothing
        """
        print("-----------Игрок: {} --------------".format(self.player.name))
        self.player.show_card()
        print("--------------------------------------------")

        print("-----------Игрок: {} ---------------".format(self.comp.name))
        self.comp.show_card()
        print("--------------------------------------------")


    def __iter__(self):
        return self

    def __next__(self):
        """
        Represent a game situation of every turn
        :return: iterator
        """

        self.__show_game()

        drum = self.get_drum()

        print("Следующий бочонок номер {}.".format(drum))

        inp = ""

        #if a player misses the y/n key it will show input field again
        while inp != "y" and inp != "n":
            inp = input("Зачеркнуть цифру? (y/n): ").lower()

        cmp_check = self.comp.check_card(drum)
        pl_check = self.player.check_card(drum)


        if cmp_check == "all":
            self.__show_game()
            return "Выиграл компьютер"

        if pl_check == "one" and inp == "n":
            return "Выиграл компьютер"

        if pl_check is False and inp == "y":
            return "Выиграл компьютер"

        if pl_check == "all" and inp == "y":
            self.__show_game()
            return "Выиграл {}".format(self.player.name)

        return False



game = Game("Шастин Павел")

win = False

while win is False:
    win = next(game)

print(win)




