import asyncio
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import json
from db import (init_db, pdf_report, pdf_report_course, check_user_in_db, check_admin_in_db,
                check_admin_password, add_user_to_db, generate_password, add_admin_to_db, generate_users_pdf,
                generate_admins_pdf, add_illness,  generate_illness_stats_by_course, generate_illness_stats,
                get_illness_ids, add_message_db, get_message_ids_not_answered, get_message_names_by_ids,
                get_message_messages_by_name, add_reply, set_answered_messages, get_reply_no_watched,
                check_statsman_in_db, check_statsman_password, add_statsman, generate_statsmans_pdf, save_food_answers,
                save_pain_answers, save_physical_answers, save_daytime_answers, save_psycho_answers, add_tg_id_admin,
                add_tg_id_user, add_tg_id_statsman)

import zipfile
from keyboards import (kb_1_30, kb_2, kb_3_4_10_14, kb_5_13,
                       kb_6, kb_7_8_9_11_20_22_23_26_28, kb_12, kb_15_17_24_25, kb_16,
                       kb_18_19, kb_29, kb_21_27, kb_admin, kb_main_menu, kb_admin_course_choose, kb_admin_users, kb_back_users,
                       kb_students_admins, kb_back, kb_choose_type, kb_admin_ill_choose, kb_years,
                       kb_admin_group_choose, kb_admin_user_choose, kb_names, kb_spam, kb_statsman_menu)

bot = Bot(token='6735071514:AAHE1uVzht-JYxDEHoCvd7s7nvtwJQ5Vzls')
dp = Dispatcher()
save_folder = 'Spravki'
os.makedirs(save_folder, exist_ok=True)
pdf_folder = 'Files pdf'
os.makedirs(pdf_folder, exist_ok=True)
png_folder = 'Files png'
os.makedirs(png_folder, exist_ok=True)


class Autorization(StatesGroup):
    Login = State()
    Password = State()
    AdminPassword = State()
    Start_autorization = State()


class AdminStates(StatesGroup):
    Admin_menu = State()
    Test_or_illness = State()
    Illness_course_choose = State()
    Users_work = State()
    Illness_date_choose = State()
    Illness_user_choose = State()
    Illness_choose_course = State()
    Illness_choose_course_group = State()
    Illness_choose_year = State()
    Illness_choose_year_course = State()
    Illness_group_choose = State()
    Course_choose = State()
    Group_choose = State()
    Choose_admin_user = State()
    Choose_course_user = State()
    Choose_group_user = State()
    Choose_message = State()
    Answer = State()


class AddUser(StatesGroup):
    user_first_name = State()
    user_last_name = State()
    user_group = State()
    user_course = State()
    admin_first_name = State()
    admin_last_name = State()
    statsman_first_name = State()
    statsman_last_name = State()


class UserStates(StatesGroup):
    User_menu = State()
    Send_date = State()
    Send_photo = State()
    Send_Message = State()


class StatsmanStates(StatesGroup):
    Statsman_menu = State()
    Illness_choose_course = State()
    Illness_choose_year = State()
    Illness_choose_course_group = State()
    Illness_choose_year_course = State()
    Course_choose = State()
    Group_choose = State()


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

active_admins_ids = []


def log(tg_id, action):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(f"User logs/{tg_id}_log.txt", "a", encoding="utf-8") as txt:
        txt.write(f"[{now}] {action}\n")


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    await message.answer('Добро пожаловать в приложения мониторинга здоровья обучающихся!')
    await message.answer('Введите логин.')
    await state.set_state(Autorization.Login)
    log(tg_id, "/start")


@dp.message(Command("help"))
async def send_help(message: types.Message):
    help_text = (
        "Помощь в работе с ботом. \n"
        "команда  /start - перезапустит бота"
    )
    await message.answer(help_text)


@dp.message(Autorization.Start_autorization)
async def start_autorization(message: Message, state: FSMContext):
    await message.answer('Введите логин.')
    await state.set_state(Autorization.Login)


@dp.message(Autorization.Login)
async def handle_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    tg_id = message.from_user.id
    log(tg_id, full_name)
    try:
        name, surname = full_name.split()
    except ValueError:
        await message.answer('Неверный логин.')
        return

    user = check_user_in_db(name, surname)
    admin = check_admin_in_db(name, surname)
    statsman = check_statsman_in_db(name, surname)

    if user:
        user_id, _, _, _, group, course = user
        await state.update_data(user_id=user_id, name=name, surname=surname, group=group, course=course)
    elif admin or statsman:
        await state.update_data(name=name, surname=surname)

    if user and admin and statsman:
        await message.answer('Введите пароль.')
    elif user and admin:
        await message.answer('Введите пароль.')
    elif statsman and user:
        await message.answer('Введите пароль.')
    elif admin and statsman:
        await message.answer('Введите пароль.')
    elif user or admin or statsman:
        await message.answer('Введите пароль.')
    else:
        await message.answer('Неверный логин.')
        await state.set_state(Autorization.Login)
        return

    await state.set_state(Autorization.Password)


@dp.message(Autorization.Password)
async def handle_password(message: Message, state: FSMContext):
    password = message.text.strip()
    tg_id = message.from_user.id
    log(tg_id, password)
    user_data = await state.get_data()
    name = user_data.get('name')
    surname = user_data.get('surname')
    user = check_user_in_db(name, surname)
    if user:
        user_id, _, _, student_password, group, course = user

        if student_password == password:
            await state.update_data(user_id=user_id, name=name, surname=surname, group=group, course=course)
            add_tg_id_user(tg_id,name, surname, password)
            await message.answer(f'Вы авторизовались как {name} {surname}. Выберите одну из опции.',
                                 reply_markup=kb_main_menu())

            await state.set_state(UserStates.User_menu)
            return

    admin = check_admin_in_db(name, surname)
    if admin:
        if check_admin_password(name, surname, password):
            tg_id = message.from_user.id
            active_admins_ids.append(tg_id)
            await state.clear()
            add_tg_id_admin(tg_id,name, surname, password)
            await message.answer(f'Вы авторизовались как {name} {surname}. Выберите одну из опции.',
                                 reply_markup=kb_admin())
            await state.set_state(AdminStates.Admin_menu)
            return

    statsman = check_statsman_in_db(name, surname)
    if statsman:
        if check_statsman_password(name, surname, password):
            await state.set_state(StatsmanStates.Statsman_menu)
            add_tg_id_statsman(tg_id,name, surname, password)
            await message.answer(f"Вы авторизовались как статистик {name} {surname}!Выберите 1 из опций.",
                                 reply_markup=kb_statsman_menu())
            return

    await message.answer('Неверный пароль. Попробуйте снова.')
    await state.set_state(Autorization.Password)


@dp.callback_query(AdminStates.Admin_menu)
async def admin_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    data = callback.data
    log(tg_id, data)
    if data == "Результаты":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer("Раздел просмотра аналитики по тестированию и болезням.",
                                         reply_markup=kb_choose_type())
        await state.set_state(AdminStates.Test_or_illness)
    elif data == "Справки":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer("Раздел просмотра справок от обучающихся. Справки каких курсов вы хотите просмотреть?",
                                         reply_markup=kb_admin_course_choose())
        await state.set_state(AdminStates.Illness_course_choose)
    elif data == "Пользователи":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
    elif data == "Входящие сообщения":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        ids = get_message_ids_not_answered()
        names = get_message_names_by_ids(ids)
        await callback.message.answer("Выберите сообщение от пользователя", reply_markup=kb_names(names))
        await state.set_state(AdminStates.Choose_message)
    elif data == "Выход":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        if tg_id in active_admins_ids:
            active_admins_ids.remove(tg_id)
        await callback.message.answer('Введите логин.')
        await state.set_state(Autorization.Login)

    await callback.answer()


@dp.message(AdminStates.Illness_course_choose)
async def illness_course_choose(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Все курсы":
        await message.answer("Выбраны все курсы, все группы и все пользователи."
                             "Введите дату в формает XX.XX.XXXX или же диапозон дат в формает"
                             "XX.XX.XXXX - XX.XX.XXXX")
        await state.update_data(illness_course="all")
        await state.update_data(illness_group="all")
        await state.update_data(illness_users="all")
        await state.set_state(AdminStates.Illness_date_choose)
    if message.text == "1":
        await message.answer("1 курс", reply_markup=kb_admin_group_choose(1, True))
        await state.update_data(illness_course="1")
        await state.set_state(AdminStates.Illness_group_choose)
    if message.text == "2":
        await message.answer("2 курс", reply_markup=kb_admin_group_choose(2, True))
        await state.update_data(illness_course="2")
        await state.set_state(AdminStates.Illness_group_choose)
    if message.text == "3":
        await message.answer("3 курс", reply_markup=kb_admin_group_choose(3, True))
        await state.update_data(illness_course="3")
        await state.set_state(AdminStates.Illness_group_choose)
    if message.text == "4":
        await message.answer("4 курс", reply_markup=kb_admin_group_choose(4, True))
        await state.update_data(illness_course="4")
        await state.set_state(AdminStates.Illness_group_choose)
    if message.text == "Назад":
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Вы авторизовались как администратор. Выберите одну из опции.',
                             reply_markup=kb_admin())

        await state.set_state(AdminStates.Admin_menu)


@dp.message(AdminStates.Illness_group_choose)
async def illness_group_choose(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    data = await state.get_data()
    course = data.get("illness_course")
    group = message.text.strip()
    if group == "Все группы":
        await message.answer("Выбраны все группы и все пользователи."
                             "Введите дату в формает XX.XX.XXXX или же диапозон дат в формает"
                             "XX.XX.XXXX - XX.XX.XXXX")
        await state.update_data(illness_group="all")
        await state.update_data(illness_users="all")
        await state.set_state(AdminStates.Illness_date_choose)
        return
    if group == "Назад":
        await message.answer("Раздел просмотра справок от обучающихся. Справки каких курсов вы хотите просмотреть?",
                             reply_markup=kb_admin_course_choose())
        await state.set_state(AdminStates.Illness_course_choose)
        return

    await message.answer(f"{group}", reply_markup=kb_admin_user_choose(course, group))
    await state.update_data(illness_group=group)
    await state.set_state(AdminStates.Illness_user_choose)


@dp.message(AdminStates.Illness_user_choose)
async def illness_user_choose(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    user_message = message.text.strip()
    if user_message == "Все пользователи":
        await message.answer("Выбраны все пользователи. Введите дату в формает XX.XX.XXXX или же диапозон дат в формает"
                             "XX.XX.XXXX - XX.XX.XXXX")
        await state.update_data(illness_users="all")
        await state.set_state(AdminStates.Illness_date_choose)
        return
    if message.text == "Назад":
        await message.answer("Раздел просмотра справок от обучающихся. Справки каких курсов вы хотите просмотреть?",
                             reply_markup=kb_admin_course_choose())
        await state.set_state(AdminStates.Illness_course_choose)
    else:
        await message.answer(f"Выбран{user_message}. Введите дату в формает XX.XX.XXXX или же диапозон дат в формаете"
                             "XX.XX.XXXX - XX.XX.XXXX")
        await state.update_data(illness_users=user_message)
        await state.set_state(AdminStates.Illness_date_choose)


@dp.message(AdminStates.Illness_date_choose)
async def illness_date_choose(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    user_message = message.text.strip()
    if user_message == "Назад":
        await message.answer("Раздел просмотра справок от обучающихся. Справки каких курсов вы хотите просмотреть?",
                             reply_markup=kb_admin_course_choose())
        await state.set_state(AdminStates.Illness_course_choose)
        return
    if len(user_message) == 23:
        data = await state.get_data()
        course = data.get("illness_course")
        group = data.get("illness_group")
        name = data.get("illness_users")
        ids = get_illness_ids(str(course), str(group), str(name), user_message)
        await message.answer(f"Архив .zip со справками по заданным параметрам. {ids}")

        if os.path.exists('Spravki/illness_photos.zip'):
            os.remove('Spravki/illness_photos.zip')

        with zipfile.ZipFile('Spravki/illness_photos.zip', "w") as zipf:
            for doc_id in ids:
                filename = f"{doc_id}.jpg"
                filepath = os.path.join("Spravki", filename)
                if os.path.exists(filepath):
                    zipf.write(filepath, arcname=filename)

        zip_file = FSInputFile('Spravki/illness_photos.zip')
        await message.answer_document(zip_file)
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Вы авторизовались как администратор. Выберите одну из опции.',
                             reply_markup=kb_admin())
        await state.set_state(AdminStates.Admin_menu)
    else:
        await message.answer("Неправильный формат даты!"
                             "Укажите дату начала и конца болезни в формате XX.XX.XXXX - XX.XX.XXXX")


@dp.message(AdminStates.Test_or_illness)
async def test_or_illness(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Тестирование":
        await message.answer("Раздел просмотра аналтики тестирования. Выберите курс.",
                             reply_markup=kb_admin_course_choose())
        await state.set_state(AdminStates.Course_choose)
    elif message.text == "Болезни":
        await message.answer("Раздел просмотра аналтики болезней.", reply_markup=kb_admin_ill_choose())
        await state.set_state(AdminStates.Illness_choose_course)
    if message.text == "Назад":
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Вы авторизовались как администратор. Выберите одну из опции.',
                             reply_markup=kb_admin())
        await state.set_state(AdminStates.Admin_menu)


@dp.message(AdminStates.Illness_choose_course)
async def illness_choose_course(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Статистика по месяцам за год все курсы":
        await message.answer("Выберите учбеный год", reply_markup=kb_years())
        await state.set_state(AdminStates.Illness_choose_year)
    if message.text == "Статистика по месяцам за год 1 курс":
        await state.update_data(ill_course=1)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(1, True))
        await state.set_state(AdminStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 2 курс":
        await state.update_data(ill_course=2)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(2, True))
        await state.set_state(AdminStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 3 курс":
        await state.update_data(ill_course=3)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(3, True))
        await state.set_state(AdminStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 4 курс":
        await state.update_data(ill_course=4)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(4, True))
        await state.set_state(AdminStates.Illness_choose_course_group)
    if message.text == "Назад":
        await message.answer("Раздел просмотра информации о пользователях.", reply_markup=kb_choose_type())
        await state.set_state(AdminStates.Test_or_illness)


@dp.message(AdminStates.Illness_choose_course_group)
async def illness_choose_year_course(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    group = message.text.strip()
    if group == "Назад":
        await message.answer("Раздел просмотра аналтики болезней.", reply_markup=kb_admin_ill_choose())
        await state.set_state(AdminStates.Illness_choose_course)
        return
    await state.update_data(group=group)
    await message.answer("Выберите учбеный год", reply_markup=kb_years())
    await state.set_state(AdminStates.Illness_choose_year_course)


@dp.message(AdminStates.Illness_choose_year_course)
async def illness_choose_year_course(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "2023 - 2024":
        data = await state.get_data()
        course_num = data.get('ill_course')
        group = data.get('group')
        group_name = group.replace("/", "_")
        generate_illness_stats_by_course(course_num, str(group), "2023 - 2024")
        pdf_file = FSInputFile(f'Files pdf/illness_stats_course_{course_num}_{group_name}_2023-2024.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за год курс - {course_num}, группа - {group}"
                             f"  2023 - 2024")
        await message.answer_document(pdf_file)
    if message.text == "2024 - 2025":
        data = await state.get_data()
        course_num = data.get('ill_course')
        group = data.get('group')
        group_name = group.replace("/", "_")
        generate_illness_stats_by_course(course_num, str(group), "2024 - 2025")
        pdf_file = FSInputFile(f'Files pdf/illness_stats_course_{course_num}_{group_name}_2024-2025.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за год {course_num} курс 2024 - 2025")
        await message.answer_document(pdf_file)
    if message.text == "2025 - 2026":
        data = await state.get_data()
        course_num = data.get('ill_course')
        group = data.get('group')
        group_name = group.replace("/", "_")
        generate_illness_stats_by_course(course_num, str(group), "2025 - 2026")
        pdf_file = FSInputFile(f'Files pdf/illness_stats_course_{course_num}_{group_name}_2025-2026.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за год {course_num} курс 2025 - 2026")
        await message.answer_document(pdf_file)
    if message.text == "2026 - 2027":
        data = await state.get_data()
        course_num = data.get('ill_course')
        group = data.get('group')
        group_name = group.replace("/", "_")
        generate_illness_stats_by_course(course_num, str(group), "2026 - 2027")
        pdf_file = FSInputFile(f'Files pdf/illness_stats_course_{course_num}_{group_name}_2026-2027.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за год {course_num} курс 2026 - 2027")
        await message.answer_document(pdf_file)
    if message.text == "Назад":
        await message.answer("Раздел просмотра аналтики болезней.", reply_markup=kb_admin_ill_choose())
        await state.set_state(AdminStates.Illness_choose_course)


@dp.message(AdminStates.Illness_choose_year)
async def illness_choose_year(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "2023 - 2024":
        generate_illness_stats(str("2023 - 2024"))
        pdf_file = FSInputFile(f'Files pdf/illness_stats2023-2024.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за 2023 - 2024 год")
        await message.answer_document(pdf_file)
    if message.text == "2024 - 2025":
        generate_illness_stats(str("2024 - 2025"))
        pdf_file = FSInputFile(f'Files pdf/illness_stats2024-2025.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за 2024 - 2025 год")
        await message.answer_document(pdf_file)
    if message.text == "2025 - 2026":
        generate_illness_stats(str("2025 - 2026"))
        pdf_file = FSInputFile(f'Files pdf/illness_stats2025-2026.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за 2025 - 2026 год")
        await message.answer_document(pdf_file)
    if message.text == "2026 - 2027":
        generate_illness_stats(str("2026 - 2027"))
        pdf_file = FSInputFile(f'Files pdf/illness_stats2026-2027.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за 2026 - 2027 год")
        await message.answer_document(pdf_file)
    if message.text == "Назад":
        await message.answer("Раздел просмотра аналтики болезней.", reply_markup=kb_admin_ill_choose())
        await state.set_state(AdminStates.Illness_choose_course)


@dp.message(AdminStates.Course_choose)
async def course_choose(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Все курсы":
        pdf_report()
        pdf_file = FSInputFile("Files pdf/Answers_Report.pdf")
        await message.answer("Отчет по всем курсам")
        await message.answer_document(pdf_file)
    elif message.text == "1":
        await state.update_data(test_course="1")
        await state.set_state(AdminStates.Group_choose)
        await message.answer("выбран 1 курс выберите группу", reply_markup=kb_admin_group_choose(1, True))
    elif message.text == "2":
        await state.update_data(test_course="2")
        await state.set_state(AdminStates.Group_choose)
        await message.answer("выбран 2 курс выберите группу", reply_markup=kb_admin_group_choose(1, True))
    elif message.text == "3":
        await state.update_data(test_course="3")
        await state.set_state(AdminStates.Group_choose)
        await message.answer("выбран 3 курс выберите группу", reply_markup=kb_admin_group_choose(1, True))
    elif message.text == "4":
        await state.update_data(test_course="4")
        await state.set_state(AdminStates.Group_choose)
        await message.answer("выбран 4 курс выберите группу", reply_markup=kb_admin_group_choose(1, True))
    elif message.text == "Назад":
        await state.set_state(AdminStates.Test_or_illness)
        await message.answer("Раздел просмотра информации о пользователях.", reply_markup=kb_choose_type())


@dp.message(AdminStates.Group_choose)
async def group_choose(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    group = message.text.strip()
    if group == "Все группы":
        data = await state.get_data()
        course = data.get("test_course")
        pdf_report_course(course, "all")
        pdf_file = FSInputFile(f"Files pdf/Statistic_{course}_all.pdf")
        await message.answer(f"Отчет по {course} курсу")
        await message.answer_document(pdf_file)
        return
    elif group == "Назад":
        await message.answer("Раздел просмотра аналтики тестирования. Выберите курс.",
                             reply_markup=kb_admin_course_choose())
        await state.set_state(AdminStates.Course_choose)
        return

    data = await state.get_data()
    course = data.get("test_course")
    pdf_report_course(course, group)
    group_label = group.replace("/", "_")
    pdf_file = FSInputFile(f"Files pdf/Statistic_{course}_{group_label}.pdf")
    await message.answer("Отчет по первому курсу")
    await message.answer_document(pdf_file)


@dp.message(AdminStates.Users_work)
async def users_work(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Список пользователей":
        await message.answer("Выберите список пользователей", reply_markup=kb_students_admins())
        await state.set_state(AdminStates.Choose_admin_user)
    elif message.text == "Добавить ученика":
        await message.answer("Введите имя пользователя:",  reply_markup=kb_back_users())
        await state.set_state(AddUser.user_first_name)
    elif message.text == "Добавить работника":
        await message.answer("Введите имя работника:", reply_markup=kb_back_users())
        await state.set_state(AddUser.admin_first_name)
    elif message.text == "Добавить аналитика":
        await message.answer("Введите имя работника:", reply_markup=kb_back_users())
        await state.set_state(AddUser.statsman_first_name)
    elif message.text == "Назад":
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Вы авторизовались как администратор. Выберите одну из опции.',
                             reply_markup=kb_admin())
        await state.set_state(AdminStates.Admin_menu)


@dp.message(AdminStates.Choose_admin_user)
async def choose_admin_user(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Студенты":
        await message.answer("Выберите курс", reply_markup=kb_admin_course_choose())
        await state.set_state(AdminStates.Choose_course_user)
    elif message.text == "Администраторы":
        generate_admins_pdf()
        pdf_file = FSInputFile("Files pdf/admins.pdf")
        await message.answer("Список администраторов")
        await message.answer_document(pdf_file)
    elif message.text == "Аналитики":
        generate_statsmans_pdf()
        pdf_file = FSInputFile("Files pdf/statsmans.pdf")
        await message.answer("Список аналитиков")
        await message.answer_document(pdf_file)
    elif message.text == "Назад":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)


@dp.message(AdminStates.Choose_course_user)
async def choose_course_user(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    course = message.text.strip()
    if course == "Все курсы":
        generate_users_pdf("all", "all")
        pdf_file = FSInputFile("Files pdf/users.pdf")
        await message.answer("Список всех студентов")
        await message.answer_document(pdf_file)
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return
    elif course == "Назад":
        await message.answer("Выберите список пользователей", reply_markup=kb_students_admins())
        await state.set_state(AdminStates.Choose_admin_user)
        return
    await state.update_data(course=course)
    await message.answer(f"Выберите группу {course} курса", reply_markup=kb_admin_group_choose(int(course), True))
    await state.set_state(AdminStates.Choose_group_user)


@dp.message(AdminStates.Choose_group_user)
async def choose_group_user(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    group = message.text.strip()
    if group == "Назад":
        await message.answer("Выберите курс", reply_markup=kb_admin_course_choose())
        await state.set_state(AdminStates.Choose_course_user)
        return
    data = await state.get_data()
    course = data.get('course')
    generate_users_pdf(course, group)
    pdf_file = FSInputFile("Files pdf/users.pdf")
    await message.answer(f"Список студентов куср - {course}, группы - {group}")
    await message.answer_document(pdf_file)
    await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
    await state.set_state(AdminStates.Users_work)


@dp.message(AddUser.user_first_name)
async def get_user_first_name(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return

    await state.update_data(first_name=message.text.strip())
    await message.answer("Введите фамилию пользователя:")
    await state.set_state(AddUser.user_last_name)


@dp.message(AddUser.user_last_name)
async def get_user_last_name(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return

    await state.update_data(last_name=message.text.strip())
    await message.answer("Выберите курс пользователя:", reply_markup=kb_admin_course_choose())
    await state.set_state(AddUser.user_course)


@dp.message(AddUser.user_course)
async def get_user_course(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    course = message.text.strip()
    if course == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return

    await state.update_data(course=course)
    await message.answer("Выберите группу пользователя.", reply_markup=kb_admin_group_choose(int(course), False))
    await state.set_state(AddUser.user_group)


@dp.message(AddUser.user_group)
async def get_user_group(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    group = message.text.strip()
    if group == "Назад":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return

    data = await state.get_data()

    add_user_to_db(
        data['first_name'],
        data['last_name'],
        generate_password(),
        group,
        int(data['course']))

    await message.answer("Пользователь успешно добавлен.")
    await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
    await state.set_state(AdminStates.Users_work)


@dp.message(AddUser.statsman_first_name)
async def get_statsman_first_name(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return

    await state.update_data(statsman_first_name=message.text.strip())
    await message.answer("Введите фамилию пользователя:")
    await state.set_state(AddUser.statsman_last_name)


@dp.message(AddUser.statsman_last_name)
async def get_statsman_last_name(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return

    await state.update_data(statsman_last_name=message.text.strip())
    data = await state.get_data()
    add_statsman(data['statsman_first_name'], data['statsman_last_name'], generate_password())

    await message.answer("Аналитик добавлен в базу.", reply_markup=kb_admin_users())
    await state.set_state(AdminStates.Users_work)


@dp.message(AddUser.admin_first_name)
async def get_admin_first_name(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return

    await state.update_data(admin_first_name=message.text.strip())
    await message.answer("Введите фамилию пользователя:")
    await state.set_state(AddUser.admin_last_name)


@dp.message(AddUser.admin_last_name)
async def get_admin_last_name(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Вернутся в меню работы с пользователями":
        await message.answer("Меню для работы с пользователями бота", reply_markup=kb_admin_users())
        await state.set_state(AdminStates.Users_work)
        return

    await state.update_data(admin_last_name=message.text.strip())
    data = await state.get_data()

    add_admin_to_db(
        data['admin_first_name'],
        data['admin_last_name'],
        generate_password())

    await message.answer("Работник добавлен в базу.", reply_markup=kb_admin_users())
    await state.set_state(AdminStates.Users_work)


@dp.message(AdminStates.Choose_message)
async def choose_message(message: types.Message, state: FSMContext):
    tg_id_n = message.from_user.id
    log(tg_id_n, message.text.strip())
    name = message.text.strip()
    if name == "Назад":
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Вы авторизовались как администратор. Выберите одну из опции.',
                             reply_markup=kb_admin())
        await state.set_state(AdminStates.Admin_menu)
        return
    tg_id, messages = get_message_messages_by_name(name)
    await message.answer(f"Сообщения от {name}")
    await state.update_data(tg_id_user=tg_id)
    await state.update_data(name_user=name)
    for msg in messages:
        await message.answer(msg)
    await message.answer("Напишите ваше сообщение.", reply_markup=kb_spam)
    await state.set_state(AdminStates.Answer)


@dp.message(AdminStates.Answer)
async def answer(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    admin_answer = message.text.strip()
    tg_id_admin = message.from_user.id
    data = await state.get_data()
    tg_id_user = data.get("tg_id_user")
    name = data.get("name_user")
    ids = get_message_ids_not_answered()
    names = get_message_names_by_ids(ids)
    if admin_answer == "Назад":
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Вы авторизовались как администратор. Выберите одну из опции.',
                             reply_markup=kb_admin())
        await state.set_state(AdminStates.Admin_menu)
        return
    if admin_answer == "Пометить как спам!":
        add_reply(tg_id_user, tg_id_admin, "Помечено как спам!", "no")
        set_answered_messages(tg_id_user)
        await bot.send_message(tg_id_user, f"{name}, ваше сообщение было помечено как спам.")
        await message.answer("Выберите cообщение от пользователя", reply_markup=kb_names(names))
        await state.set_state(AdminStates.Choose_message)
        return

    add_reply(tg_id_user, tg_id_admin, admin_answer, "нет")
    set_answered_messages(tg_id_user)
    await bot.send_message(tg_id_user,  "вам пришло сообщение от администратора. Проверьте сообщения.")
    names_new = get_message_names_by_ids(ids)
    await message.answer("Выберите cообщение от пользователя", reply_markup=kb_names(names_new))
    await state.set_state(AdminStates.Choose_message)


@dp.callback_query(UserStates.User_menu)
async def handle_main_menu(callback: types.CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    action = callback.data.strip()
    log(tg_id, action)
    if action == "Пройти тестирование о здоровье":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer(
            "Тестирование начинается. Тест состоит из 30 вопросов. Хорошо подумайте над ответами. "
            "После завершения тестирования ответы запишутся. Тестирование можно пройти повторно,"
            "предыдущие ответы будут перезаписаны."
        )
        await ask_question(callback.message, state, 1, kb_1_30)
        await state.set_state(Questions.question_1)
    elif action == "Прикрепить справку":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer(
            "Укажите дату начала и конца болезни в формате XX.XX.XXXX - XX.XX.XXXX",
            reply_markup=kb_back()
        )
        await state.set_state(UserStates.Send_date)
    elif action == "Отправить сообщение работнику.":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer("Введите свое сообщение работнику.", reply_markup=kb_back())
        await state.set_state(UserStates.Send_Message)
    elif action == "Входящие сообщения":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        messages = get_reply_no_watched(tg_id)
        if not messages:
            await callback.message.answer("У вас нет новых сообщений!")
        else:
            await callback.message.answer(f"Просмотр входящих сообщений {len(messages)}.")
            for msg in messages:
                await callback.message.answer(msg)
    elif action == "Выход":
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer('Введите логин.')
        await state.set_state(Autorization.Login)

    await callback.answer()


@dp.message(UserStates.Send_date)
async def send_date(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    date = message.text.strip()
    if date == "Назад":
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите одну из опции.',
                             reply_markup=kb_main_menu())
        await state.set_state(UserStates.User_menu)
        return
    if len(date) == 23:
        await state.update_data(date=date)
        await message.answer("Прикрепите справку", reply_markup=kb_back())
        await state.set_state(UserStates.Send_photo)
    else:
        await message.answer("Неправильный формат даты!"
                             "Укажите дату начала и конца болезни в формате XX.XX.XXXX - XX.XX.XXXX")


@dp.message(UserStates.Send_photo)
async def send_photo(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, "Отправлено фото")
    if message.photo:
        photo = message.photo[-1]
        file = await message.bot.get_file(photo.file_id)
        file_path = file.file_path
        data = await state.get_data()
        name = data.get('name')
        surname = data.get('surname')
        date = datetime.now().date()
        illness_id = add_illness(name + " " + surname, data.get('group'), data.get('course'), data.get('date'), date)
        filename = f"{illness_id}.jpg"
        save_path = os.path.join(save_folder, filename)
        await message.bot.download_file(file_path, save_path)
        await message.answer("Справка отправлена")
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите одну из опции.', reply_markup=kb_main_menu())
        await state.set_state(UserStates.User_menu)
    elif message.text == "Назад":
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите одну из опции.', reply_markup=kb_main_menu())
        await state.set_state(UserStates.User_menu)


@dp.message(UserStates.Send_Message)
async def send_message(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    msg = message.text.strip()
    if msg == "Назад":
        await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Вы авторизовались как пользователь. Выберите одну из опции.',
                             reply_markup=kb_main_menu())
        await state.set_state(UserStates.User_menu)
        return
    tg_id = message.from_user.id
    data = await state.get_data()
    first_name = data.get('name')
    surname = data.get('surname')
    name = first_name + " " + surname
    add_message_db(name, tg_id, msg)
    await message.answer("Ваше сообщение отправлено!")
    for admin in active_admins_ids:
        await bot.send_message(admin, "Потсупило новое сообщение!")
    await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Вы авторизовались как {name} {surname}. Выберите одну из опции.', reply_markup=kb_main_menu())
    await state.set_state(UserStates.User_menu)


@dp.message(StatsmanStates.Statsman_menu)
async def statsman_menu(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == 'Статистика по тестированию':
        await message.answer("Раздел просмотра аналтики тестирования. Выберите курс.",
                             reply_markup=kb_admin_course_choose())
        await state.set_state(StatsmanStates.Course_choose)
    if message.text == "Статистика по болезням":
        await message.answer("Раздел просмотра аналтики болезней.", reply_markup=kb_admin_ill_choose())
        await state.set_state(StatsmanStates.Illness_choose_course)


@dp.message(StatsmanStates.Course_choose)
async def statsman_course_choose(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Все курсы":
        pdf_report()
        pdf_file = FSInputFile("Files pdf/Answers_Report.pdf")
        await message.answer("Отчет по всем курсам")
        await message.answer_document(pdf_file)
    elif message.text == "1":
        await state.update_data(test_course="1")
        await state.set_state(StatsmanStates.Group_choose)
        await message.answer("выбран 1 курс выберите группу", reply_markup=kb_admin_group_choose(1, True))
    elif message.text == "2":
        await state.update_data(test_course="2")
        await state.set_state(StatsmanStates.Group_choose)
        await message.answer("выбран 2 курс выберите группу", reply_markup=kb_admin_group_choose(1, True))
    elif message.text == "3":
        await state.update_data(test_course="3")
        await state.set_state(StatsmanStates.Group_choose)
        await message.answer("выбран 3 курс выберите группу", reply_markup=kb_admin_group_choose(1, True))
    elif message.text == "4":
        await state.update_data(test_course="4")
        await state.set_state(StatsmanStates.Group_choose)
        await message.answer("выбран 4 курс выберите группу", reply_markup=kb_admin_group_choose(1, True))
    elif message.text == "Назад":
        await state.set_state(StatsmanStates.Statsman_menu)
        await message.answer("меню статсман", reply_markup=kb_statsman_menu())


@dp.message(StatsmanStates.Group_choose)
async def statsman_group_choose(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    group = message.text.strip()
    if group == "Все группы":
        data = await state.get_data()
        course = data.get("test_course")
        pdf_report_course(course, "all")
        pdf_file = FSInputFile(f"Files pdf/Statistic_{course}_all.pdf")
        await message.answer(f"Отчет по {course} курсу")
        await message.answer_document(pdf_file)
        return
    elif group == "Назад":
        await message.answer("Раздел просмотра аналтики тестирования. Выберите курс.",
                             reply_markup=kb_statsman_menu())
        await state.set_state(StatsmanStates.Statsman_menu)
        return

    data = await state.get_data()
    course = data.get("test_course")
    pdf_report_course(course, group)
    group_label = group.replace("/", "_")
    pdf_file = FSInputFile(f"Files pdf/Statistic_{course}_{group_label}.pdf")
    await message.answer("Отчет по первому курсу")
    await message.answer_document(pdf_file)


@dp.message(StatsmanStates.Illness_choose_course)
async def statsman_illness_choose_course(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Статистика по месяцам за год все курсы":
        await message.answer("Выберите учбеный год", reply_markup=kb_years())
        await state.set_state(StatsmanStates.Illness_choose_year)
    if message.text == "Статистика по месяцам за год 1 курс":
        await state.update_data(ill_course=1)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(1, True))
        await state.set_state(StatsmanStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 2 курс":
        await state.update_data(ill_course=2)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(2, True))
        await state.set_state(StatsmanStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 3 курс":
        await state.update_data(ill_course=3)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(3, True))
        await state.set_state(StatsmanStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 4 курс":
        await state.update_data(ill_course=4)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(4, True))
        await state.set_state(StatsmanStates.Illness_choose_course_group)
    if message.text == "Назад":
        await message.answer("Раздел просмотра информации о пользователях.", reply_markup=kb_statsman_menu())
        await state.set_state(StatsmanStates.Statsman_menu)


@dp.message(StatsmanStates.Illness_choose_year_course)
async def statsman_illness_choose_year_course(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "2023 - 2024":
        data = await state.get_data()
        course_num = data.get('ill_course')
        group = data.get('group')
        group_name = group.replace("/", "_")
        generate_illness_stats_by_course(course_num, str(group), "2023 - 2024")
        pdf_file = FSInputFile(f'Files pdf/illness_stats_course_{course_num}_{group_name}_2023-2024.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за год курс - {course_num}, группа - {group}"
                             f"  2023 - 2024")
        await message.answer_document(pdf_file)
    if message.text == "2024 - 2025":
        data = await state.get_data()
        course_num = data.get('ill_course')
        group = data.get('group')
        group_name = group.replace("/", "_")
        generate_illness_stats_by_course(course_num, str(group), "2024 - 2025")
        pdf_file = FSInputFile(f'Files pdf/illness_stats_course_{course_num}_{group_name}_2024-2025.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за год {course_num} курс 2024 - 2025")
        await message.answer_document(pdf_file)
    if message.text == "2025 - 2026":
        data = await state.get_data()
        course_num = data.get('ill_course')
        group = data.get('group')
        group_name = group.replace("/", "_")
        generate_illness_stats_by_course(course_num, str(group), "2025 - 2026")
        pdf_file = FSInputFile(f'Files pdf/illness_stats_course_{course_num}_{group_name}_2025-2026.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за год {course_num} курс 2025 - 2026")
        await message.answer_document(pdf_file)
    if message.text == "2026 - 2027":
        data = await state.get_data()
        course_num = data.get('ill_course')
        group = data.get('group')
        group_name = group.replace("/", "_")
        generate_illness_stats_by_course(course_num, str(group), "2026 - 2027")
        pdf_file = FSInputFile(f'Files pdf/illness_stats_course_{course_num}_{group_name}_2026-2027.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за год {course_num} курс 2026 - 2027")
        await message.answer_document(pdf_file)
    if message.text == "Назад":
        await message.answer("Раздел просмотра аналтики болезней.", reply_markup=kb_admin_ill_choose())
        await state.set_state(StatsmanStates.Illness_choose_course)


@dp.message(StatsmanStates.Illness_choose_course_group)
async def statsman_illness_choose_year_course(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    group = message.text.strip()
    if group == "Назад":
        await message.answer("Раздел просмотра аналтики болезней.", reply_markup=kb_admin_ill_choose())
        await state.set_state(StatsmanStates.Illness_choose_course)
        return
    await state.update_data(group=group)
    await message.answer("Выберите учбеный год", reply_markup=kb_years())
    await state.set_state(StatsmanStates.Illness_choose_year_course)


@dp.message(StatsmanStates.Illness_choose_course)
async def statsman_illness_choose_course(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "Статистика по месяцам за год все курсы":
        await message.answer("Выберите учбеный год", reply_markup=kb_years())
        await state.set_state(StatsmanStates.Illness_choose_year)
    if message.text == "Статистика по месяцам за год 1 курс":
        await state.update_data(ill_course=1)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(1, True))
        await state.set_state(StatsmanStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 2 курс":
        await state.update_data(ill_course=2)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(2, True))
        await state.set_state(StatsmanStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 3 курс":
        await state.update_data(ill_course=3)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(3, True))
        await state.set_state(StatsmanStates.Illness_choose_course_group)
    if message.text == "Статистика по месяцам за год 4 курс":
        await state.update_data(ill_course=4)
        await message.answer("Выберите группу", reply_markup=kb_admin_group_choose(4, True))
        await state.set_state(StatsmanStates.Illness_choose_course_group)
    if message.text == "Назад":
        await message.answer("Раздел просмотра информации о пользователях.", reply_markup=kb_statsman_menu())
        await state.set_state(StatsmanStates.Statsman_menu)


@dp.message(StatsmanStates.Illness_choose_year)
async def illness_choose_year(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    if message.text == "2023 - 2024":
        generate_illness_stats(str("2023 - 2024"))
        pdf_file = FSInputFile(f'Files pdf/illness_stats2023-2024.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за 2023 - 2024 год")
        await message.answer_document(pdf_file)
    if message.text == "2024 - 2025":
        generate_illness_stats(str("2024 - 2025"))
        pdf_file = FSInputFile(f'Files pdf/illness_stats2024-2025.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за 2024 - 2025 год")
        await message.answer_document(pdf_file)
    if message.text == "2025 - 2026":
        generate_illness_stats(str("2025 - 2026"))
        pdf_file = FSInputFile(f'Files pdf/illness_stats2025-2026.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за 2025 - 2026 год")
        await message.answer_document(pdf_file)
    if message.text == "2026 - 2027":
        generate_illness_stats(str("2026 - 2027"))
        pdf_file = FSInputFile(f'Files pdf/illness_stats2026-2027.pdf')
        await message.answer(f"Статистика заболеваний по месяцам за 2026 - 2027 год")
        await message.answer_document(pdf_file)
    if message.text == "Назад":
        await message.answer("меню", reply_markup=kb_statsman_menu())
        await state.set_state(StatsmanStates.Statsman_menu)


async def ask_question(message: Message, state: FSMContext, question_number: int, markup):
    question_text = questions.get(str(question_number))
    await message.answer(question_text, reply_markup=markup)
    await state.update_data(question_number=question_number)


@dp.message(Questions.question_1)
async def question_1(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_1=message.text.strip())
    await ask_question(message, state, 2, kb_2)
    await state.set_state(Questions.question_2)


@dp.message(Questions.question_2)
async def question_2(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_2=message.text.strip())
    await ask_question(message, state, 3, kb_3_4_10_14)
    await state.set_state(Questions.question_3)


@dp.message(Questions.question_3)
async def question_3(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_3=message.text.strip())
    await ask_question(message, state, 4, kb_3_4_10_14)
    await state.set_state(Questions.question_4)


@dp.message(Questions.question_4)
async def question_4(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_4=message.text.strip())
    await ask_question(message, state, 5, kb_5_13)
    await state.set_state(Questions.question_5)


@dp.message(Questions.question_5)
async def question_5(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_5=message.text)
    await ask_question(message, state, 6, kb_6)
    await state.set_state(Questions.question_6)


@dp.message(Questions.question_6)
async def question_6(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_6=message.text)
    await ask_question(message, state, 7, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_7)


@dp.message(Questions.question_7)
async def question_7(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_7=message.text)
    await ask_question(message, state, 8, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_8)


@dp.message(Questions.question_8)
async def question_8(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_8=message.text)
    await ask_question(message, state, 9, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_9)


@dp.message(Questions.question_9)
async def question_9(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_9=message.text)
    await ask_question(message, state, 10, kb_3_4_10_14)
    await state.set_state(Questions.question_10)


@dp.message(Questions.question_10)
async def question_10(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_10=message.text)
    await ask_question(message, state, 11, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_11)


@dp.message(Questions.question_11)
async def question_11(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_11=message.text)
    await ask_question(message, state, 12, kb_12)
    await state.set_state(Questions.question_12)


@dp.message(Questions.question_12)
async def question_12(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_12=message.text)
    await ask_question(message, state, 13, kb_5_13)
    await state.set_state(Questions.question_13)


@dp.message(Questions.question_13)
async def question_13(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_13=message.text)
    await ask_question(message, state, 14, kb_3_4_10_14)
    await state.set_state(Questions.question_14)


@dp.message(Questions.question_14)
async def question_14(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_14=message.text)
    await ask_question(message, state, 15, kb_15_17_24_25)
    await state.set_state(Questions.question_15)


@dp.message(Questions.question_15)
async def question_15(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_15=message.text)
    await ask_question(message, state, 16, kb_16)
    await state.set_state(Questions.question_16)


@dp.message(Questions.question_16)
async def question_16(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_16=message.text)
    await ask_question(message, state, 17, kb_15_17_24_25)
    await state.set_state(Questions.question_17)


@dp.message(Questions.question_17)
async def question_17(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_17=message.text)
    await ask_question(message, state, 18, kb_18_19)
    await state.set_state(Questions.question_18)


@dp.message(Questions.question_18)
async def question_18(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_18=message.text)
    await ask_question(message, state, 19, kb_18_19)
    await state.set_state(Questions.question_19)


@dp.message(Questions.question_19)
async def question_19(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_19=message.text)
    await ask_question(message, state, 20, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_20)


@dp.message(Questions.question_20)
async def question_20(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_20=message.text)
    await ask_question(message, state, 21, kb_21_27)
    await state.set_state(Questions.question_21)


@dp.message(Questions.question_21)
async def question_21(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_21=message.text)
    await ask_question(message, state, 22, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_22)


@dp.message(Questions.question_22)
async def question_22(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_22=message.text)
    await ask_question(message, state, 23, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_23)


@dp.message(Questions.question_23)
async def question_23(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_23=message.text)
    await ask_question(message, state, 24, kb_15_17_24_25)
    await state.set_state(Questions.question_24)


@dp.message(Questions.question_24)
async def question_24(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_24=message.text)
    await ask_question(message, state, 25, kb_15_17_24_25)
    await state.set_state(Questions.question_25)


@dp.message(Questions.question_25)
async def question_25(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_25=message.text)
    await ask_question(message, state, 26, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_26)


@dp.message(Questions.question_26)
async def question_26(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_26=message.text)
    await ask_question(message, state, 27, kb_21_27)
    await state.set_state(Questions.question_27)


@dp.message(Questions.question_27)
async def question_27(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_27=message.text)
    await ask_question(message, state, 28, kb_7_8_9_11_20_22_23_26_28)
    await state.set_state(Questions.question_28)


@dp.message(Questions.question_28)
async def question_28(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_28=message.text)
    await ask_question(message, state, 29, kb_29)
    await state.set_state(Questions.question_29)


@dp.message(Questions.question_29)
async def question_29(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_29=message.text)
    await ask_question(message, state, 30, kb_1_30)
    await state.set_state(Questions.question_30)


@dp.message(Questions.question_30)
async def question_30(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    log(tg_id, message.text.strip())
    await state.update_data(answer_30=message.text)
    data = await state.get_data()
    login = data.get('name') + " " + data.get('surname')
    save_food_answers(
        tg_id,
        login,
        data.get('course'),
        data.get('group'),
        data.get('answer_1'),
        data.get('answer_2'),
        data.get('answer_3'),
        data.get('answer_4'),
        data.get('answer_5'),
        data.get('answer_6'))

    save_pain_answers(
        tg_id,
        login,
        data.get('course'),
        data.get('group'),
        data.get('answer_7'),
        data.get('answer_8'),
        data.get('answer_9'),
        data.get('answer_10'),
        data.get('answer_11'),
        data.get('answer_12'))

    save_physical_answers(
        tg_id,
        login,
        data.get('course'),
        data.get('group'),
        data.get('answer_13'),
        data.get('answer_14'),
        data.get('answer_15'),
        data.get('answer_16'),
        data.get('answer_17'))

    save_daytime_answers(
        tg_id,
        login,
        data.get('course'),
        data.get('group'),
        data.get('answer_18'),
        data.get('answer_19'),
        data.get('answer_20'),
        data.get('answer_21'),
        data.get('answer_22'))

    save_psycho_answers(
        tg_id,
        login,
        data.get('course'),
        data.get('group'),
        data.get('answer_23'),
        data.get('answer_24'),
        data.get('answer_25'),
        data.get('answer_26'),
        data.get('answer_27'),
        data.get('answer_28'),
        data.get('answer_29'),
        data.get('answer_30'))

    await message.answer("Тест пройден.Ответы сохранены.", reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Возвращение в главное меню", reply_markup=ReplyKeyboardRemove())
    await message.answer("Вы успешно авторизовались. Пожалуйста, выберите одну из опций.", reply_markup=kb_main_menu()
    )

    await state.set_state(UserStates.User_menu)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

