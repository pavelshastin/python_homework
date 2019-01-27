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

curr_dir_store = os.path.join(os.getcwd(), "curr_dir.txt")

if (os.path.exists(curr_dir_store)):
    with open(curr_dir_store, "r", encoding="UTF-8") as f:
        curr_dir = f.read().strip()
else:
    curr_dir = os.getcwd()


print('sys.argv = ', sys.argv)


def print_help():
    print("help - получение справки")
    print("mkdir <dir_name> - создание директории")
    print("ping - тестовый ключ")


def make_dir():
    if not dir_name:
        print("Необходимо указать имя директории вторым параметром")
        return
    dir_path = os.path.join(curr_dir, dir_name)
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

        dir_includes = os.listdir(curr_dir)
        print(curr_dir)
        print(dir_includes)

        copy_files = [re.match(match_str, f).groups() for f in dir_includes if re.match(match_str, f)]

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
            copy_name = os.path.join(curr_dir, file_name[0] + "_copy." + file_name[1])

        print(copy_files, copy_name, curr_dir)

        copyfile(os.path.join(curr_dir, sys.argv[2]), copy_name)

    except IndexError:
        print("No file name given")
    except FileExistsError:
        print("The file {} doesn't exists in directory {} or file name is not correct.".format(file_name, os.getcwd()))



def remove_file():
    try:
        file_name = sys.argv[2]

        if os.path.exists(file_name):
            confirm = input("Do you realy want to delete {} Y/N".format(file_name))

            if confirm.tolower() == "y":
                os.remove(file_name)
                print("File is deleted")
            else:
                print("The file deleting is aborted")
        else:
            raise FileExistsError('No such file found')
    except IndexError:
        print("No file name given")


def change_dir():
    try:
        dir_name = sys.argv[2]

        os.chdir(curr_dir)

        os.chdir(dir_name)


        with open(curr_dir_store, "w", encoding="UTF-8") as f:
            f.write(os.getcwd())

        print(os.getcwd())

    except IndexError:
        print("No directory path is given")
    except OSError:
        print("The given directory doesn't exist")


def full_path():
    try:
        if sys.argv[2]:
            print("The ls command doesn't require any arguments")
            return

    except IndexError:
        print(os.path.abspath(curr_dir))


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