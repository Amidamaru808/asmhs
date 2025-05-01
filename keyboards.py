from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import get_users


all_groups = {
    1: ["ИД 23.1/Б3-24", "ИД 23.1/Б4-24", "ИД 23.1/Б1-24", "ИД 30.1/Б4-24", "ИД 30.1/Б3-24", "ИДc 23.1/Б3-24",
        "УД 21.1/Б3-24", "УД 21.1/Б6-24", "УД 21.1/Б13-24", "УД 25.1/Б1-24", "УД 29.1/Б1-24", "НД 36.1/Б1-24",
        "УД 14.1/1-24", "УДс 21.1/Б2-24", "УДс 21.1/Б3-24", "УДс 21.1/Б6-24", "ЭД 20.1/Б10-24", "ЭД 32.1/Б1-24",
        "ЭД 13.1/1-24", "ЭД 13.2/1-24", "ЭД 24.1/Б2-24", "ЭДс 20.1/Б10-24", "ЭД 20.1/Б11-24", "ЭДс 20.1/Б2-24",
        "ЭДс 32.1/Б11-24", "ЮД 22.1/Б2-24", "ЮД 22.1/Б3-24", "ЮД 22.1/Б5-24", "ЮДc 22.1/Б2-24", "ЮДс 22.1/Б3-24",
        "УД 28.1/Б1-24", "УДс 28.1/Б1-24"],
    2: ["ИД 30.1/Б3-23", "ИД 23.1/Б3-23", "ИДc 23.1/Б3-23", "УД 21.1/Б2-23", "УД 21.1/Б3-23", "УД 25.1/Б1-23",
        "УД 25.2/Б1-23", "УД 29.1/Б1-23", "УДс 21.1/Б2-23", "УДс 21.1/Б3-23", "УДс 21.1/Б6-23", "ЭД 20.1/Б10-23",
        "ЭД 32.1/Б1-23", "ЭД 13.1/1-23", "ЭД 13.2/1-23", "ЭД 13.3/1-23", "ЭД 24.1/Б2-23", "ЭД 14.1/1-23",
        "ЭДс 20.1/Б11-23", "ЮД 22.1/Б2-23", "ЮД 22.1/Б3-23", "ЮДс 22.1/Б2-23", "УД 28.1/Б1-23", "УД 37.1/Б1-23",
        "УДс 28.1/Б1-23"],
    3: ["ИД 30.1/Б3-22", "ИД 23.1/Б3-22", "ИДс 23.1/Б3-22", "УД 21.1/Б2-22", "УД 25.1/Б1-22", "ЭД 20.1/Б10-22",
        "ЭД 32.1/Б1-22", "ЭД 13.1/1-22", "ЭД 13.2/1-22", "ЭД 13.3/1-22", "ЭДс 20.1/Б10-22", "ЮД 22.1/Б2-22",
        "ЮД 22.1/Б3-22", "ЮДс 22.1/Б2-22", "УД 28.1/Б1-22"],
    4: ["ИД 23.1/Б3-21", "ИД 23.2/Б3-21", "ИД 23.3/Б3-21", "ИД 23.1/Б1-21", "ИД 30.1/Б3-21", "о. УД 29.1/Б1-21",
        "о. УД 25.1/Б1-21", "о. УД 25.2/Б1-21", "о. ЭД 20.1/Б11-21", "о. ЭД 32.1/Б1-21", "о. ЭД 13.1/1-21",
        "о. ЭД 13.2/1-21", "о. ЭД 13.3/1-21", "о. ЭД 13.4/1-21", "о. ЭД 13.5/1-21", "о. ЮД 22.1/Б2-21",
        "о. ЮД 22.1/Б3-21"]
}

def KB_back_users():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернутся в меню работы с пользователями")]
        ],
    )


def KB_back():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")]
        ],
    )


def KB_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пройти тестирование о здоровье")],
            [KeyboardButton(text="Прикрепить справку")],
            [KeyboardButton(text="3")],
            [KeyboardButton(text="4")]
        ],
    )


def KB_admin():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Результаты')],
            [KeyboardButton(text='Справки')],
            [KeyboardButton(text='Пользователи')],
            [KeyboardButton(text='Справка о работе приложения')]
        ],
    )

def KB_students_admins():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Студенты')],
            [KeyboardButton(text='Администраторы')],
            [KeyboardButton(text='Назад')]
        ],
    )

def KB_years():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='2023 - 2024'),
                                         KeyboardButton(text='2024 - 2025'),
                                         KeyboardButton(text="2025 - 2026"),
                                         KeyboardButton(text="2026 - 2027"),
                                          KeyboardButton(text="Назад")]])


def KB_admin_course_choose():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Все курсы')],
                                           [KeyboardButton(text='1'),
                                           KeyboardButton(text='2')],
                                           [KeyboardButton(text='3'),
                                           KeyboardButton(text='4')],
                                           [KeyboardButton(text='Назад')]])


def KB_admin_group_choose(course, all_gr):
    groups = all_groups.get(course, [])
    keyboard = []

    if all_gr:
        keyboard.append([KeyboardButton(text='Все группы')])

    line = []
    for i, group_name in enumerate(groups):
        line.append(KeyboardButton(text=group_name))
        if (i + 1) % 3 == 0:
            keyboard.append(line)
            line = []
    if line:
        keyboard.append(line)

    keyboard.append([KeyboardButton(text='Назад')])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def KB_admin_user_choose(course, group):
    users = get_users(course, group)

    keyboard = []
    for user in users:
        keyboard.append([KeyboardButton(text=user)])

    keyboard.append([KeyboardButton(text="Все пользователи")])
    keyboard.append([KeyboardButton(text="Назад")])

    return ReplyKeyboardMarkup(keyboard=keyboard)


def KB_admin_ill_choose():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Статистика по месяцам за год 1 курс'),
                                           KeyboardButton(text='Статистика по месяцам за год 2 курс')],
                                           [KeyboardButton(text='Статистика по месяцам за год 3 курс'),
                                           KeyboardButton(text='Статистика по месяцам за год 4 курс')],
                                           [KeyboardButton(text='Статистика по месяцам за год все курсы'),
                                            KeyboardButton(text='Назад')]])


def KB_admin_users():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Список пользователей')],
                                           [KeyboardButton(text='Добавить ученика')],
                                           [KeyboardButton(text='Добавить работника')],
                                          [KeyboardButton(text="Назад")]])


def KB_choose_type():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Тестирование'),
                                         KeyboardButton(text="Болезни"),
                                          KeyboardButton(text="Назад")]])


KB_1234 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'),
                                           KeyboardButton(text='2')],
                                           [KeyboardButton(text='3'),
                                           KeyboardButton(text='4+')]])


KB_yes_no = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да')],
                                           [KeyboardButton(text='Нет')]])


KB_05_1_15_2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='0.5'),
                                           KeyboardButton(text='1')],
                                           [KeyboardButton(text='1.5'),
                                           KeyboardButton(text='2')]])


KB_chastota_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Никогда'),
                                           KeyboardButton(text='Редко')],
                                           [KeyboardButton(text='Часто'),
                                           KeyboardButton(text='Очень часто')]])


KB_chastota_2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каждый День'),
                                           KeyboardButton(text='3-4 раза в неделю')],
                                           [KeyboardButton(text='1-2 раза в неделю'),
                                           KeyboardButton(text='Не занимаюсь')]])


KB_chastota_3 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1-2 часа'),
                                           KeyboardButton(text='3-4 часа')],
                                           [KeyboardButton(text='5-6 часов'),
                                           KeyboardButton(text='7 и более часов')]])


KB_kachestvo = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ужасно'),
                                           KeyboardButton(text='Плохо')],
                                           [KeyboardButton(text='Хорошо'),
                                           KeyboardButton(text='Отлично')]])


KB_ves = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='< 40'),
                                           KeyboardButton(text='40-60')],
                                           [KeyboardButton(text='60-80'),
                                           KeyboardButton(text='80-100')]])


KB_legko = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Легко'),
                                           KeyboardButton(text='Нормально')],
                                           [KeyboardButton(text='Трудно'),
                                           KeyboardButton(text='Очень тяжело')]])


KB_druzya = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Нет друзей'),
                                           KeyboardButton(text='Мало')],
                                           [KeyboardButton(text='Достаточно'),
                                           KeyboardButton(text='Много')]])

