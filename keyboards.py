from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import get_users


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
                                           [KeyboardButton(text='1 курс')],
                                           [KeyboardButton(text='2 курс')],
                                           [KeyboardButton(text='3 курс')],
                                           [KeyboardButton(text='4 курс')],
                                           [KeyboardButton(text='Назад')]])


def KB_admin_group_choose():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Все группы')],
                                           [KeyboardButton(text='1 группа')],
                                           [KeyboardButton(text='2 группа')],
                                           [KeyboardButton(text='3 группа')],
                                           [KeyboardButton(text='4 группа')],
                                           [KeyboardButton(text='Назад')]])


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

