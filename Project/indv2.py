#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вариант 2
Самостоятельно изучите работу с пакетом click для построения
интерфейса командной строки (CLI). Использовать словарь,
содержащий следующие ключи: фамилия и инициалы;  номер группы;
успеваемость (список из пяти элементов).
Написать программу, выполняющую следующие действия:
ввод с клавиатуры данных в список, состоящий из словарей заданной
структуры; записи должны быть упорядочены по возрастанию среднего
балла;вывод на дисплей фамилий и номеров групп для всех студентов,
имеющих оценки 4 и 5; если таких студентов нет, вывести
соответствующее сообщение. Необходимо реализовать интерфейс
командной строки с использованием пакета click.
"""
import json
import os.path

import click


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


@click.command()
@click.argument("filename")
@click.option("--surname", "-sn", type=str, help="The student's surname")
@click.option("--group_number", "-gn", type=int, help="The student's group")
@click.option("--grades", "-g", multiple=True, type=list, help="grades")
@click.argument("command", type=click.Choice(["add", "display", "select"]))
def main(filename, surname, group_number, grades, command):
    is_dirty = False

    students = load_students(filename) if os.path.exists(filename) else []

    if command == "add":
        add_student(students, surname, group_number, grades)
        is_dirty = True
    elif command == "display":
        display_students(students)
    elif command == "select":
        selected = select_students(students)
        display_students(selected)

    if is_dirty:
        save_students(filename, students)


if __name__ == "__main__":
    main()
