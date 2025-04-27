import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import sqlite3
import json
from fpdf import FPDF
from db import (init_db, save_answers, pdf_report, pdf_report_course, check_user_in_db, check_admin_in_db,
                check_admin_password, add_user_to_db, generate_password, add_admin_to_db, generate_users_pdf,
                generate_admins_pdf)

from openpyxl import Workbook
from keyboards import (KB_05_1_15_2, KB_1234, KB_druzya, KB_kachestvo,
                       KB_legko, KB_yes_no, KB_ves, KB_chastota_1, KB_chastota_2,
                       KB_chastota_3, KB_admin, KB_main_menu, KB_admin_choose, KB_admin_users, KB_back_users,
                       KB_students_admins)

bot = Bot(token='6735071514:AAHE1uVzht-JYxDEHoCvd7s7nvtwJQ5Vzls')
dp = Dispatcher()


class Autorization(StatesGroup):
    Login = State()
    Password = State()
    AdminPassword = State()


class AddStudent(StatesGroup):
    user_first_name = State()
    user_last_name = State()
    user_group = State()
    user_course = State()


class AddAdmin(StatesGroup):
    admin_first_name = State()
    admin_last_name = State()


class Questions(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()
    question_11 = State()
    question_12 = State()
    question_13 = State()
    question_14 = State()
    question_15 = State()
    question_16 = State()
    question_17 = State()
    question_18 = State()
    question_19 = State()
    question_20 = State()
    question_21 = State()
    question_22 = State()
    question_23 = State()
    question_24 = State()
    question_25 = State()
    question_26 = State()
    question_27 = State()
    question_28 = State()
    question_29 = State()
    question_30 = State()


def load_questions():
    with open('TestQuestions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions


questions = load_questions()
init_db()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Введите логин.')
    await state.set_state(Autorization.Login)


@dp.message(Autorization.Login)
async def handle_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    try:
        name, surname = full_name.split()
    except ValueError:
        await message.answer('Неверный логин.')
        return

    user = check_user_in_db(name, surname)
    admin = check_admin_in_db(name, surname)

    if user and admin:
        await message.answer(f'{name} {surname}, Введите пароль.')
        user_id, _, _, user_password, group, course = user
        await state.update_data(user_id=user_id, name=name, surname=surname, group=group, course=course)
        await state.set_state(Autorization.Password)

    elif user:
        user_id, name, surname, password, group, course = user
        await state.update_data(user_id=user_id, name=name, surname=surname, group=group, course=course)
        await message.answer('Введите пароль.')
        await state.set_state(Autorization.Password)

    elif admin:
        await state.update_data(name=name, surname=surname)
        await message.answer('Введите пароль.')
        await state.set_state(Autorization.Password)

    else:
        await message.answer('Неверный логин.')
        await state.set_state(Autorization.Login)


@dp.message(Autorization.Password)
async def handle_password(message: Message, state: FSMContext):
    password = message.text.strip()
    user_data = await state.get_data()
    name = user_data.get('name')
    surname = user_data.get('surname')
    user = check_user_in_db(name, surname)
    if user:
        user_id, _, _, student_password, group, course = user

        if student_password == password:
            await state.update_data(user_id=user_id, name=name, surname=surname, group=group, course=course)
            await message.answer(f'Вы авторизовались как {name} {surname}. Выберите одну из опции.',
                                 reply_markup=KB_main_menu())
            await state.set_state('main_menu')
            return

    admin = check_admin_in_db(name, surname)
    if admin:
        if check_admin_password(name, surname, password):
            await state.clear()
            await message.answer(f'Вы авторизовались как {name} {surname}. Выберите одну из опции.',
                                 reply_markup=KB_admin())
            await state.set_state('admin_menu')
            return

    await message.answer('Неверный пароль. Попробуйте снова.')
    await state.set_state(Autorization.Password)


@dp.message(StateFilter("admin_menu"))
async def admin_menu(message: types.Message, state: FSMContext):
    if message.text == "Результаты":
        await message.answer("Выберите по какому курсы хотите посмотреть ответы.", reply_markup=KB_admin_choose())
        await state.set_state('course_choose')
    elif message.text == "Кнопка 2":
        await message.answer("Кнопка 2")
    elif message.text == "Пользователи":
        await message.answer("Меню для работы с пользователями бота", reply_markup=KB_admin_users())
        await state.set_state('users_work')
    elif message.text == "Справка о работе приложения":
        await message.answer("тут будет справка о работе приложения")


@dp.message(StateFilter("course_choose"))
async def course_choose(message: types.Message, state: FSMContext):
    if message.text == "Все курсы":
        pdf_report()
        pdf_file = FSInputFile("Answers_Report.pdf")
        await message.answer("Отчет по всем курсам")
        await message.answer_document(pdf_file)
    elif message.text == "1":
        pdf_report_course(1)
        pdf_file = FSInputFile("Statistic_1_course.pdf")
        await message.answer("Отчет по первому курсу")
        await message.answer_document(pdf_file)
    elif message.text == "2":
        pdf_report_course(2)
        pdf_file = FSInputFile("Statistic_2_course.pdf")
        await message.answer("Отчет по второму курсу")
        await message.answer_document(pdf_file)
    elif message.text == "3":
        pdf_report_course(3)
        pdf_file = FSInputFile("Statistic_3_course.pdf")
        await message.answer("Отчет по третьему курсу")
        await message.answer_document(pdf_file)
    elif message.text == "4":
        pdf_report_course(4)
        pdf_file = FSInputFile("Statistic_4_course.pdf")
        await message.answer("Отчет по четвертому курсу")
        await message.answer_document(pdf_file)
    elif message.text == "Назад":
        await state.set_state('admin_menu')
        await message.answer(f'Выберите одну из опции.', reply_markup=KB_admin())


@dp.message(StateFilter("users_work"))
async def users_work(message: types.Message, state: FSMContext):
    if message.text == "Список пользователей":
        await message.answer("Выберите список пользователей", reply_markup=KB_students_admins())
        await state.set_state("choose_admin_user")
    elif message.text == "Добавить ученика":
        await message.answer("Введите имя пользователя:",  reply_markup=KB_back_users())
        await state.set_state(AddStudent.user_first_name)
    elif message.text == "Добавить работника":
        await message.answer("Введите имя работника:", reply_markup=KB_back_users())
        await state.set_state(AddAdmin.admin_first_name)
    elif message.text == "Назад":
        await message.answer(f'Вы авторизовались как администратор. Выберите одну из опции.',
                             reply_markup=KB_admin())
        await state.set_state('admin_menu')


@dp.message(StateFilter("choose_admin_user"))
async def choose_admin_user(message: types.Message, state: FSMContext):
    if message.text == "Студенты":
        generate_users_pdf()
        pdf_file = FSInputFile("users.pdf")
        await message.answer("Список студентов")
        await message.answer_document(pdf_file)
    elif message.text == "Администраторы":
        generate_admins_pdf()
        pdf_file = FSInputFile("admins.pdf")
        await message.answer("Список администраторов")
        await message.answer_document(pdf_file)
    elif message.text == "Назад":
        await message.answer("Меню для работы с пользователями бота", reply_markup=KB_admin_users())
        await state.set_state('users_work')


@dp.message(AddStudent.user_first_name)
async def get_user_first_name(message: Message, state: FSMContext):
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=KB_admin_users())
        await state.set_state('users_work')
        return

    await state.update_data(first_name=message.text.strip())
    await message.answer("Введите фамилию пользователя:")
    await state.set_state(AddStudent.user_last_name)


@dp.message(AddStudent.user_last_name)
async def get_user_last_name(message: Message, state: FSMContext):
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=KB_admin_users())
        await state.set_state('users_work')
        return

    await state.update_data(last_name=message.text.strip())
    await message.answer("Введите группу пользователя:")
    await state.set_state(AddStudent.user_group)


@dp.message(AddStudent.user_group)
async def get_user_group(message: Message, state: FSMContext):
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=KB_admin_users())
        await state.set_state('users_work')
        return

    await state.update_data(group=message.text.strip())
    await message.answer("Введите курс пользователя:")
    await state.set_state(AddStudent.user_course)


@dp.message(AddStudent.user_course)
async def get_user_course(message: Message, state: FSMContext):
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=KB_admin_users())
        await state.set_state('users_work')
        return

    await state.update_data(course=message.text.strip())
    data = await state.get_data()

    add_user_to_db(
        data['first_name'],
        data['last_name'],
        generate_password(),
        data['group'],
        int(data['course']))

    await message.answer("Пользователь добавлен в базу.", reply_markup=KB_admin_users())
    await state.set_state('users_work')


@dp.message(AddAdmin.admin_first_name)
async def get_admin_first_name(message: Message, state: FSMContext):
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=KB_admin_users())
        await state.set_state('users_work')
        return

    await state.update_data(admin_first_name=message.text.strip())
    await message.answer("Введите фамилию пользователя:")
    await state.set_state(AddAdmin.admin_last_name)


@dp.message(AddAdmin.admin_last_name)
async def get_admin_last_name(message: Message, state: FSMContext):
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=KB_admin_users())
        await state.set_state('users_work')
        return

    await state.update_data(admin_last_name=message.text.strip())
    data = await state.get_data()

    add_admin_to_db(
        data['admin_first_name'],
        data['admin_last_name'],
        generate_password())

    await message.answer("Работник добавлен в базу.", reply_markup=KB_admin_users())
    await state.set_state('users_work')


@dp.message(StateFilter("main_menu"))
async def handle_main_menu(message: types.Message, state: FSMContext):
    if message.text == "Пройти тестирование о здоровье":
        await message.answer("Тестирование начинается. Тест состоит из 30 вопросов. Хорошо подумайте над ответами."
                             "После завершения тестирования ответы запишутся. Тестирование можно пройти повторно,"
                             "предыдущие ответы будут перезаписаны.")
        await state.set_state('test_health')
        await ask_question(message, state, 1, KB_1234)
        await state.set_state(Questions.question_1)
    elif message.text == "2":
        await message.answer("2")
    elif message.text == "3":
        await message.answer("3")
    elif message.text == "4":
        await message.answer("4")




async def ask_question(message: Message, state: FSMContext, question_number: int, markup):
    question_text = questions.get(str(question_number))
    await message.answer(question_text, reply_markup=markup)
    await state.update_data(question_number=question_number)


@dp.message(Questions.question_1)
async def question_1(message: Message, state: FSMContext):
    await state.update_data(answer_1=message.text.strip())
    await ask_question(message, state, 2, KB_1234)
    await state.set_state(Questions.question_2)


@dp.message(Questions.question_2)
async def question_2(message: Message, state: FSMContext):
    await state.update_data(answer_2=message.text.strip())
    await ask_question(message, state, 3, KB_yes_no)
    await state.set_state(Questions.question_3)


@dp.message(Questions.question_3)
async def question_3(message: Message, state: FSMContext):
    await state.update_data(answer_3=message.text.strip())
    await ask_question(message, state, 4, KB_yes_no)
    await state.set_state(Questions.question_4)


@dp.message(Questions.question_4)
async def question_4(message: Message, state: FSMContext):
    await state.update_data(answer_4=message.text.strip())
    await ask_question(message, state, 5, KB_1234)
    await state.set_state(Questions.question_5)


@dp.message(Questions.question_5)
async def question_5(message: Message, state: FSMContext):
    await state.update_data(answer_5=message.text)
    await ask_question(message, state, 6, KB_05_1_15_2)
    await state.set_state(Questions.question_6)


@dp.message(Questions.question_6)
async def question_6(message: types.Message, state: FSMContext):
    await state.update_data(answer_6=message.text)
    await ask_question(message, state, 7, KB_chastota_1)
    await state.set_state(Questions.question_7)


@dp.message(Questions.question_7)
async def question_7(message: types.Message, state: FSMContext):
    await state.update_data(answer_7=message.text)
    await ask_question(message, state, 8, KB_chastota_1)
    await state.set_state(Questions.question_8)


@dp.message(Questions.question_8)
async def question_8(message: types.Message, state: FSMContext):
    await state.update_data(answer_8=message.text)
    await ask_question(message, state, 9, KB_chastota_1)
    await state.set_state(Questions.question_9)


@dp.message(Questions.question_9)
async def question_9(message: types.Message, state: FSMContext):
    await state.update_data(answer_9=message.text)
    await ask_question(message, state, 10, KB_chastota_2)
    await state.set_state(Questions.question_10)


@dp.message(Questions.question_10)
async def question_10(message: types.Message, state: FSMContext):
    await state.update_data(answer_10=message.text)
    await ask_question(message, state, 11, KB_yes_no)
    await state.set_state(Questions.question_11)


@dp.message(Questions.question_11)
async def question_11(message: types.Message, state: FSMContext):
    await state.update_data(answer_11=message.text)
    await ask_question(message, state, 12, KB_kachestvo)
    await state.set_state(Questions.question_12)


@dp.message(Questions.question_12)
async def question_12(message: types.Message, state: FSMContext):
    await state.update_data(answer_12=message.text)
    await ask_question(message, state, 13, KB_chastota_1)
    await state.set_state(Questions.question_13)


@dp.message(Questions.question_13)
async def question_13(message: types.Message, state: FSMContext):
    await state.update_data(answer_13=message.text)
    await ask_question(message, state, 14, KB_1234)
    await state.set_state(Questions.question_14)


@dp.message(Questions.question_14)
async def question_14(message: types.Message, state: FSMContext):
    await state.update_data(answer_14=message.text)
    await ask_question(message, state, 15, KB_kachestvo)
    await state.set_state(Questions.question_15)


@dp.message(Questions.question_15)
async def question_15(message: types.Message, state: FSMContext):
    await state.update_data(answer_15=message.text)
    await ask_question(message, state, 16, KB_chastota_1)
    await state.set_state(Questions.question_16)


@dp.message(Questions.question_16)
async def question_16(message: types.Message, state: FSMContext):
    await state.update_data(answer_16=message.text)
    await ask_question(message, state, 17, KB_chastota_3)
    await state.set_state(Questions.question_17)


@dp.message(Questions.question_17)
async def question_17(message: Message, state: FSMContext):
    await state.update_data(answer_17=message.text)
    await ask_question(message, state, 18, KB_ves)
    await state.set_state(Questions.question_18)


@dp.message(Questions.question_18)
async def question_18(message: Message, state: FSMContext):
    await state.update_data(answer_18=message.text)
    await ask_question(message, state, 19, KB_chastota_3)
    await state.set_state(Questions.question_19)


@dp.message(Questions.question_19)
async def question_19(message: Message, state: FSMContext):
    await state.update_data(answer_19=message.text)
    await ask_question(message, state, 20, KB_chastota_1)
    await state.set_state(Questions.question_20)


@dp.message(Questions.question_20)
async def question_20(message: Message, state: FSMContext):
    await state.update_data(answer_20=message.text)
    await ask_question(message, state, 21, KB_kachestvo)
    await state.set_state(Questions.question_21)


@dp.message(Questions.question_21)
async def question_21(message: Message, state: FSMContext):
    await state.update_data(answer_21=message.text)
    await ask_question(message, state, 22, KB_kachestvo)
    await state.set_state(Questions.question_22)


@dp.message(Questions.question_22)
async def question_22(message: Message, state: FSMContext):
    await state.update_data(answer_22=message.text)
    await ask_question(message, state, 23, KB_chastota_1)
    await state.set_state(Questions.question_23)


@dp.message(Questions.question_23)
async def question_23(message: Message, state: FSMContext):
    await state.update_data(answer_23=message.text)
    await ask_question(message, state, 24, KB_legko)
    await state.set_state(Questions.question_24)


@dp.message(Questions.question_24)
async def question_24(message: Message, state: FSMContext):
    await state.update_data(answer_24=message.text)
    await ask_question(message, state, 25, KB_yes_no)
    await state.set_state(Questions.question_25)


@dp.message(Questions.question_25)
async def question_25(message: Message, state: FSMContext):
    await state.update_data(answer_25=message.text)
    await ask_question(message, state, 26, KB_chastota_1)
    await state.set_state(Questions.question_26)


@dp.message(Questions.question_26)
async def question_26(message: Message, state: FSMContext):
    await state.update_data(answer_26=message.text)
    await ask_question(message, state, 27, KB_yes_no)
    await state.set_state(Questions.question_27)


@dp.message(Questions.question_27)
async def question_27(message: Message, state: FSMContext):
    await state.update_data(answer_27=message.text)
    await ask_question(message, state, 28, KB_druzya)
    await state.set_state(Questions.question_28)


@dp.message(Questions.question_28)
async def question_28(message: Message, state: FSMContext):
    await state.update_data(answer_28=message.text)
    await ask_question(message, state, 29, KB_legko)
    await state.set_state(Questions.question_29)


@dp.message(Questions.question_29)
async def question_29(message: Message, state: FSMContext):
    await state.update_data(answer_29=message.text)
    await ask_question(message, state, 30, None)
    await state.set_state(Questions.question_30)


@dp.message(Questions.question_30)
async def question_30(message: types.Message, state: FSMContext):
    await state.update_data(answer_30=message.text)
    data = await state.get_data()
    login = data.get('name') + data.get('surname')
    save_answers(
        login,
        data.get('group'),
        data.get('course'),
        data.get('answer_1'),
        data.get('answer_2'),
        data.get('answer_3'),
        data.get('answer_4'),
        data.get('answer_5'),
        data.get('answer_6'),
        data.get('answer_7'),
        data.get('answer_8'),
        data.get('answer_9'),
        data.get('answer_10'),
        data.get('answer_11'),
        data.get('answer_12'),
        data.get('answer_13'),
        data.get('answer_14'),
        data.get('answer_15'),
        data.get('answer_16'),
        data.get('answer_17'),
        data.get('answer_18'),
        data.get('answer_19'),
        data.get('answer_20'),
        data.get('answer_21'),
        data.get('answer_22'),
        data.get('answer_23'),
        data.get('answer_24'),
        data.get('answer_25'),
        data.get('answer_26'),
        data.get('answer_27'),
        data.get('answer_28'),
        data.get('answer_29'),
        data.get('answer_30')
    )

    await message.answer("Тест пройден.Ответы сохранены.", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Вы успешно авторизовались. Пожалуйста, выберите одну из опций.",
        reply_markup=KB_main_menu()
    )

    await state.set_state('main_menu')

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



