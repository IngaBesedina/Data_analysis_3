#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вариант 2
Использовать словарь, содержащий следующие ключи: фамилия и инициалы;
номер группы; успеваемость (список из пяти элементов).
Написать программу, выполняющую следующие действия:
ввод с клавиатуры данных в список, состоящий из словарей заданной
структуры; записи должны быть упорядочены по возрастанию среднего балла;
вывод на дисплей фамилий и номеров групп для всех студентов,
имеющих оценки 4 и 5; если таких студентов нет, вывести соответствующее
сообщение.Дополнительно реализовать интерфейс командной строки (CLI).
"""

import argparse
import json
import os.path


def add_student(staff, surname, group_number, grades):
    """
    Добавить данные о студенте.
    """
    staff.append(
        {"surname": surname, "group_number": group_number, "grades": grades}
    )

    return staff


def display_students(staff):
    """
    Отобразить список студентов.
    """
    # Проверить, что список студентов не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 14
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^14} |".format(
                "№", "Ф.И.О.", "Группа", "Оценки"
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(staff, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>14} |".format(
                    idx,
                    student.get("surname", ""),
                    student.get("group_number", ""),
                    ", ".join(str(el) for el in student.get("grades")[0]),
                )
            )
        print(line)

    else:
        print("Список студентов пуст.")


def select_students(staff):
    # Сформировать список студентов, имеющих оценки 4 и 5.
    result = []
    for student in staff:
        if all(int(grade) >= 4 for grade in student["grades"][0]):
            result.append(student)

    # Возвратить список выбранных студентов.
    return result


def save_students(file_name, staff):
    """
    Сохранить всех учеников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    """
    Загрузить всех учеников из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename", action="store", help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления студента.
    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new student"
    )
    add.add_argument(
        "-sn",
        "--surname",
        action="store",
        type=str,
        required=True,
        help="The student's surname",
    )
    add.add_argument(
        "-gn",
        "--group_number",
        action="store",
        type=int,
        help="The student's group",
    )
    add.add_argument(
        "-g",
        "--grades",
        action="store",
        nargs="+",
        type=list,
        required=True,
        help="grades",
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all students"
    )

    # Создать субпарсер для выбора студентов.
    _ = subparsers.add_parser(
        "select", parents=[file_parser], help="Select the students"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех студентов из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        students = load_students(args.filename)
    else:
        students = []

    # Добавить студента.
    if args.command == "add":
        students = add_student(
            students, args.surname, args.group_number, args.grades
        )
        is_dirty = True

    # Отобразить всех студентов.
    elif args.command == "display":
        display_students(students)

    # Выбрать требуемых студентов.
    elif args.command == "select":
        selected = select_students(students)
        display_students(selected)

    # Сохранить данные в файл, если список студентов был изменен.
    if is_dirty:
        save_students(args.filename, students)


if __name__ == "__main__":
    main()
