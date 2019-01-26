#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Задание-1:
# Доработайте реализацию программы из примера examples/5_with_args.py,
# добавив реализацию следующих команд (переданных в качестве аргументов):
#   cp <file_name> - создает копию указанного файла
#   rm <file_name> - удаляет указанный файл (запросить подтверждение операции)
#   cd <full_path or relative_path> - меняет текущую директорию на указанную
#   ls - отображение полного пути текущей директории
# путь считать абсолютным (full_path) -
# в Linux начинается с /, в Windows с имени диска,
# все остальные пути считать относительными.

# Важно! Все операции должны выполняться в той директории, в который вы находитесь.
# Исходной директорией считать ту, в которой был запущен скрипт.

# P.S. По возможности, сделайте кросс-платформенную реализацию.
import os
import re
import sys
from shutil import copyfile

print('sys.argv = ', sys.argv)


def print_help():
    print("help - получение справки")
    print("mkdir <dir_name> - создание директории")
    print("ping - тестовый ключ")


def make_dir():
    if not dir_name:
        print("Необходимо указать имя директории вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.mkdir(dir_path)
        print('директория {} создана'.format(dir_name))
    except FileExistsError:
        print('директория {} уже существует'.format(dir_name))


def ping():
    print("pong")

def copy_file():
    try:
        file_name = re.match(r"(.+)\.(\w+$)", sys.argv[2]).groups()

        match_str = r"(^{}_copy)(_\d)*\.(\w+$)".format(file_name[0])

        copy_files = [re.match(match_str, f).groups() for f in os.listdir() if re.match(match_str, f)]

        if copy_files:
            nums = []
            for file in copy_files:
                if file[1] is None:
                    copy_name = file[0] + "_1." + file[2]

                else:
                    num = int(file[1][1:])
                    nums.append(num)

            if (nums):
                cur_num = max(nums) + 1
                copy_name = file_name[0] + "_copy_{}.".format(cur_num) + file_name[1]

        else:
            copy_name = os.path.join(os.curdir, file_name[0] + "_copy." + file_name[1])

        print(copy_files, copy_name)

        copyfile(sys.argv[2], copy_name)

    except IndexError:
        print("No file name given")
    except FileExistsError:
        print("The file {} doesn't exists in directory {} or file name is not correct.".format(file_name, os.getcwd()))






def remove_file():
    pass

def change_dir():
    pass

def full_path():
    try:
        if sys.argv[2]:
            print("The ls command doesn't require any arguments")
            return

    except IndexError:
        print(os.path.abspath(os.getcwd()))


do = {
    "help": print_help,
    "mkdir": make_dir,
    "ping": ping,
    "cp": copy_file,
    "rm": remove_file,
    "cd": change_dir,
    "ls": full_path
}

try:
    dir_name = sys.argv[2]
except IndexError:
    dir_name = None

try:
    key = sys.argv[1]
except IndexError:
    key = None


if key:
    if do.get(key):
        do[key]()
    else:
        print("Задан неверный ключ")
        print("Укажите ключ help для получения справки")