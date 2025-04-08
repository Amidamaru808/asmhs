from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def KB_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Запустить тестирование")],
            [KeyboardButton(text="Кнопка 2")],
            [KeyboardButton(text="Кнопка 3")],
            [KeyboardButton(text="Кнопка 4")]
        ],
    )


def KB_admin():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Результаты')],
            [KeyboardButton(text='Кнопка 2')],
            [KeyboardButton(text='Добавить пользователя')],
            [KeyboardButton(text='Справка о работе приложения')]
        ],
    )


def KB_admin_choose():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Все курсы'),
                                           KeyboardButton(text='1'),
                                           KeyboardButton(text='2'),
                                           KeyboardButton(text='3'),
                                           KeyboardButton(text='4')]])


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

