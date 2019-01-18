# Задание-1:
# Напишите функцию, округляющую полученное произвольное десятичное число
# до кол-ва знаков (кол-во знаков передается вторым аргументом).
# Округление должно происходить по математическим правилам (0.6 --> 1, 0.4 --> 0).
# Для решения задачи не используйте встроенные функции и функции из модуля math.

def my_round(num, n):
    """
    :param num: float, number
    :param n: int, number of digits after floating point
    :return: float, rounded number according to the given after point digits
    """

    whole, decimal = str(num).split(".")

    if len(decimal) < n:
        return num

    roundPart = decimal[:n]
    restPart = decimal[n:]

    if int(restPart[0]) < 5:
        return float(whole + "." + (roundPart))
    else:

        wholePart = list(map(int, reversed(whole)))
        roundPart = list(map(int, reversed(roundPart)))

        idx = 0
        for i in roundPart:
            i += 1
            roundPart[idx] = i

            if i == 10:
                roundPart[idx] = 0

                if idx == len(roundPart) - 1:

                    idx = 0
                    for i in wholePart:
                        i += 1
                        wholePart[idx] = i

                        if i == 10:
                            wholePart[idx] = 0

                            if idx == len(wholePart) - 1:
                                wholePart.append(1)
                                break

                            idx += 1
                            continue

                        break
                idx += 1
                continue

            break

        roundPart = list(map(str, reversed(roundPart)))
        wholePart = list(map(str, reversed(wholePart)))

        return float("".join(wholePart) + "." + "".join(roundPart))



print(my_round(12.1234567, 10))
print(my_round(12.1999967, 5))
print(my_round(12.9999967, 5))
print(my_round(99.9999967, 5))
print(my_round(12.1234547, 5))


# Задание-2:
# Дан шестизначный номер билета. Определить, является ли билет счастливым.
# Решение реализовать в виде функции.
# Билет считается счастливым, если сумма его первых и последних цифр равны.
# !!!P.S.: функция не должна НИЧЕГО print'ить

def lucky_ticket(ticket_number):
    pass


print(lucky_ticket(123006))
print(lucky_ticket(12321))
print(lucky_ticket(436751))
