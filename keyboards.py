from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import get_users
from datetime import datetime

# словарь всех групп, ключ - курс 
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


#клавиатура список админов
def kb_admins_list(admins_list):
    # кнопки (пустой список) 
    keyboard = []
    for admin in admins_list:
        first_name, last_name, admin_id = admin
        button_text = f"{first_name} {last_name} ({admin_id})"
        keyboard.append([KeyboardButton(text=button_text)])

  
    #последняя кнопка - назад
    keyboard.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


#клавиатура с именами обучающихся
def kb_names(names):
    keyboard = []
    # максимум 10 кнопок
    names = names[:10]
    for i in range(0, len(names), 2):
        row = [KeyboardButton(text=name) for name in names[i:i + 2]]
        keyboard.append(row)

    keyboard.append([KeyboardButton(text="Назад")])

    return ReplyKeyboardMarkup(keyboard=keyboard)


#клавиатура 1 кнопка
def kb_back_users():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернутся в меню работы с пользователями")]
        ],
    )


# клавиатура 1 кнопка
def kb_back():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")]
        ],
    )


#главное меню обучающихся
def kb_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[

            #надпись кнопки и call back data
            [InlineKeyboardButton(text="Пройти тестирование о здоровье",
                                     callback_data="Пройти тестирование о здоровье")],
            [InlineKeyboardButton(text="Прикрепить справку", callback_data="Прикрепить справку")],
            [InlineKeyboardButton(text="Отправить сообщение работнику.",
                                     callback_data="Отправить сообщение работнику.")],
            [InlineKeyboardButton(text="Входящие сообщения", callback_data="Входящие сообщения")],
            [InlineKeyboardButton(text="Выход", callback_data="Выход")]
        ]
    )


#главное меню админов
#входные параметры - права админов
def kb_admin(results, spravki, users, messages):
    buttons = []

    if results:
        buttons.append([InlineKeyboardButton(text='Результаты', callback_data='Результаты')])
    if spravki:
        buttons.append([InlineKeyboardButton(text='Справки', callback_data='Справки')])
    if users:
        buttons.append([InlineKeyboardButton(text='Пользователи', callback_data='Пользователи')])
    if messages:
        buttons.append([InlineKeyboardButton(text='Входящие сообщения', callback_data='Входящие сообщения')])

    buttons.append([InlineKeyboardButton(text='Выход', callback_data='Выход')])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


#меню настроек прав админов
def kb_user_settings(permissions: dict) -> InlineKeyboardMarkup:
    #названия кнопок (перевод) 
    labels = {
        'results': 'Просмотр результатов',
        'spravki': 'Просмотр справок',
        'messages': 'Прием сообщений',
        'add_users': 'Добавление учеников',
        'add_admins': 'Добавление администраторов',
        'watch_users': 'Просмотр учеников',
        'watch_admins': 'Просмотр администраторов',
        'add_statsman': 'Добавление аналитиков',
        'watch_statsman': 'Просмотр аналитиков',
        'settings': 'Настройки прав'
    }

    keyboard = []
    
    # заполнение клавиатуры
    for key, value in permissions.items():
        status = "Да" if value else "Нет"
        label = labels.get(key, key)
        text = f"{label}: {status}"
        callback_data = f"toggle_{key}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back_to_admin_list')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


#клавиатуры выбора группы пользователей
#входные параметры права админа
def kb_students_admins(watch_users, watch_admins, watch_statsman):
    keyboard = []

    if watch_users:
        keyboard.append([KeyboardButton(text='Студенты')])
    if watch_admins:
        keyboard.append([KeyboardButton(text='Администраторы')])
    if watch_statsman:
        keyboard.append([KeyboardButton(text='Аналитики')])

    keyboard.append([KeyboardButton(text='Назад')])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# клавиатура выбора года
def kb_years():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='2023 - 2024'),
                                         KeyboardButton(text='2024 - 2025'),
                                         KeyboardButton(text="2025 - 2026"),
                                         KeyboardButton(text="2026 - 2027"),
                                          KeyboardButton(text="Назад")]])


#клавиатура выбора курса
#входной параметры - кнопка все курсы
def kb_admin_course_choose(all_cr):
    keyboard = []

    if all_cr:
        keyboard.append([KeyboardButton(text='Все курсы')])
    keyboard.append([
        KeyboardButton(text='1'),
        KeyboardButton(text='2')
    ])
    keyboard.append([
        KeyboardButton(text='3'),
        KeyboardButton(text='4')
    ])
    keyboard.append([KeyboardButton(text='Назад')])

    return ReplyKeyboardMarkup(keyboard=keyboard)


#выбор группы, входные параметры - номер #курса и кнопка всё группы
def kb_admin_group_choose(course, all_gr):
    #получаем значения групп по курсу
    groups = all_groups.get(course, [])
    keyboard = []

    if all_gr:
        keyboard.append([KeyboardButton(text='Все группы')])
    
    #в линию выходит по 3 группы
    line = []
    for i, group_name in enumerate(groups):
        line.append(KeyboardButton(text=group_name))
        if (i + 1) % 3 == 0:
            keyboard.append(line)
            line = []
    if line:
        keyboard.append(line)

    keyboard.append([KeyboardButton(text='Назад')])

    return ReplyKeyboardMarkup(keyboard=keyboard)

# выбор пользователя из курса и группы
def kb_admin_user_choose(course, group):
    users = get_users(course, group)

    keyboard = []
    keyboard.append([KeyboardButton(text="Все пользователи")])
    for user in users:
        keyboard.append([KeyboardButton(text=user)])

    keyboard.append([KeyboardButton(text="Назад")])

    return ReplyKeyboardMarkup(keyboard=keyboard)


def kb_admin_ill_choose():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Статистика по месяцам за год 1 курс'),
                                           KeyboardButton(text='Статистика по месяцам за год 2 курс')],
                                           [KeyboardButton(text='Статистика по месяцам за год 3 курс'),
                                           KeyboardButton(text='Статистика по месяцам за год 4 курс')],
                                           [KeyboardButton(text='Статистика по месяцам за год все курсы'),
                                            KeyboardButton(text='Назад')]])


def kb_admin_users(watch, add_users, add_admins, add_statsman, settings):
    keyboard = []

    if watch:
        keyboard.append([KeyboardButton(text='Список пользователей')])
    if add_users:
        keyboard.append([KeyboardButton(text='Добавить ученика')])
    if add_admins:
        keyboard.append([KeyboardButton(text='Добавить работника')])
    if add_statsman:
        keyboard.append([KeyboardButton(text='Добавить аналитика')])
    if settings:
        keyboard.append([KeyboardButton(text='Настройки пользователей')])

    keyboard.append([KeyboardButton(text="Назад")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def kb_choose_type():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Тестирование'),
                                         KeyboardButton(text="Болезни"),
                                          KeyboardButton(text="Назад")]])


def kb_statsman_menu():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Статистика по тестированию')],
                                          [KeyboardButton(text="Статистика по болезням")]])


kb_spam = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Пометить как спам!'),
                                         KeyboardButton(text='Назад')]])


kb_1_30 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'),
                                           KeyboardButton(text='2')],
                                           [KeyboardButton(text='3'),
                                           KeyboardButton(text='4+')]])

kb_2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1 раз в день'),
                                           KeyboardButton(text='2 раза в день')],
                                           [KeyboardButton(text='3 раза в день'),
                                           KeyboardButton(text='4 или более раз в день')]])


kb_3_4_10_14 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да')],
                                           [KeyboardButton(text='Нет')]])


kb_6 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='0.5 литров'),
                                           KeyboardButton(text='1 литров')],
                                           [KeyboardButton(text='1.5 литров'),
                                           KeyboardButton(text='2 литров')]])


kb_7_8_9_11_20_22_23_26_28 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Никогда'),
                                           KeyboardButton(text='Редко')],
                                           [KeyboardButton(text='Часто'),
                                           KeyboardButton(text='Очень часто')]])


kb_12 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='0 - 1 раз'),
                                           KeyboardButton(text='1 - 2 раза')],
                                           [KeyboardButton(text='3 - 4 раза'),
                                           KeyboardButton(text='5 и более раз')]])


kb_5_13 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каждый День'),
                                           KeyboardButton(text='3-4 раза в неделю')],
                                           [KeyboardButton(text='1-2 раза в неделю'),
                                           KeyboardButton(text='Не занимаюсь')]])


kb_18_19 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1-2 часа'),
                                           KeyboardButton(text='3-4 часа')],
                                           [KeyboardButton(text='5-6 часов'),
                                           KeyboardButton(text='7 и более часов')]])


kb_15_17_24_25 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ужасно'),
                                                KeyboardButton(text='Плохо')],
                                               [KeyboardButton(text='Хорошо'),
                                                KeyboardButton(text='Отлично')]])


kb_16 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='< 40'),
                                       KeyboardButton(text='40-60')],
                                      [KeyboardButton(text='60-80'),
                                       KeyboardButton(text='80-100')]])


kb_21_27 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Легко'),
                                         KeyboardButton(text='Нормально')],
                                         [KeyboardButton(text='Трудно'),
                                         KeyboardButton(text='Очень тяжело')]])


kb_29 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Нет друзей'),
                                       KeyboardButton(text='Мало')],
                                      [KeyboardButton(text='Достаточно'),
                                       KeyboardButton(text='Много')]])

