import sqlite3
import json
from fpdf import FPDF
import random
import string
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime


def init_db():
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                password TEXT NOT NULL,
                "group" TEXT NOT NULL,
                course INTEGER NOT NULL
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS illnesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                "group" TEXT NOT NULL,
                course INTEGER NOT NULL,
                ill_date TEXT NOT NULL,
                send_date TEXT NOT NULL
            )
        ''')

    c.execute('''
           CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tg_id INTEGER NOT NULL,
                message_text TEXT NOT NULL,
                time TEXT NOT NULL,
                answered TEXT NOT NULL
           )
       ''')

    c.execute('''
           CREATE TABLE IF NOT EXISTS reply (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_tg_user INTEGER,
                id_tg_admin INTEGER,
                answer TEXT,
                watched TEXT
           )
       ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS statsmans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS food_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id integer,
                name TEXT,
                course TEXT,
                "group" TEXT,
                answer_1 TEXT,
                answer_2 TEXT,
                answer_3 TEXT,
                answer_4 TEXT,
                answer_5 TEXT,
                answer_6 TEXT
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS pain_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id integer,
                name TEXT,
                course TEXT,
                "group" TEXT,
                answer_7 TEXT,
                answer_8 TEXT,
                answer_9 TEXT,
                answer_10 TEXT,
                answer_11 TEXT,
                answer_12 TEXT
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS physical_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id integer,
                name TEXT,
                course TEXT,
                "group" TEXT,
                answer_13 TEXT,
                answer_14 TEXT,
                answer_15 TEXT,
                answer_16 TEXT,
                answer_17 TEXT
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS daytime_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id integer,
                name TEXT,
                course TEXT,
                "group" TEXT,
                answer_18 TEXT,
                answer_19 TEXT,
                answer_20 TEXT,
                answer_21 TEXT,
                answer_22 TEXT
            )
       ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS psycho_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id integer,
                name TEXT,
                course TEXT,
                "group" TEXT,
                answer_23 TEXT,
                answer_24 TEXT,
                answer_25 TEXT,
                answer_26 TEXT,
                answer_27 TEXT,
                answer_28 TEXT,
                answer_29 TEXT,
                answer_30 TEXT
            )
       ''')

    conn.commit()
    conn.close()


def add_user_to_db(first_name, last_name, password, group, course):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (first_name, last_name, password, "group", course)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, password, group, course))
    conn.commit()
    conn.close()


def add_admin_to_db(first_name, last_name, password):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO admins (first_name, last_name, password)
        VALUES (?, ?, ?)
    ''', (first_name, last_name, password))
    conn.commit()
    conn.close()


def add_illness(name, group, course, ill_date, send_date):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO illnesses (name, "group", course, ill_date, send_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, group, course, ill_date, send_date))

    illness_id = c.lastrowid

    conn.commit()
    conn.close()
    return illness_id


def check_user_in_db(first_name, last_name):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM users WHERE first_name = ? AND last_name = ?
    ''', (first_name, last_name))
    user = c.fetchone()
    conn.close()
    return user


def check_password(name, surname, password):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''
        SELECT password FROM users WHERE first_name = ? AND last_name = ?
    ''', (name, surname))
    stored_password = c.fetchone()
    conn.close()
    if stored_password and stored_password[0] == password:
        return True
    else:
        return False


def check_admin_in_db(first_name, last_name):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM admins WHERE first_name = ? AND last_name = ?
    ''', (first_name, last_name))
    admin = c.fetchone()
    conn.close()
    return admin


def check_admin_password(first_name, last_name, password):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''
        SELECT password FROM admins WHERE first_name = ? AND last_name = ?
    ''', (first_name, last_name))
    result = c.fetchone()
    conn.close()

    if result and result[0] == password:
        return True
    else:
        return False


def load_questions(file_path='TestQuestions.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions


def save_food_answers(tg_id, name, course, group, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('DELETE FROM food_answers WHERE tg_id = ?', (tg_id,))
    c.execute('''
        INSERT INTO food_answers (tg_id, name, course, "group", answer_1, answer_2, answer_3, answer_4, answer_5, 
        answer_6)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tg_id, name, course, group, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6))
    conn.commit()
    conn.close()


def save_pain_answers(tg_id, name, course, group, answer_7, answer_8, answer_9, answer_10, answer_11, answer_12):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('DELETE FROM pain_answers WHERE tg_id = ?', (tg_id,))
    c.execute('''
        INSERT INTO pain_answers (tg_id, name, course, "group", answer_7, answer_8, answer_9, answer_10, answer_11,
         answer_12)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tg_id, name, course, group, answer_7, answer_8, answer_9, answer_10, answer_11, answer_12))
    conn.commit()
    conn.close()


def save_physical_answers(tg_id, name, course, group, answer_13, answer_14, answer_15, answer_16, answer_17):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('DELETE FROM physical_answers WHERE tg_id = ?', (tg_id,))
    c.execute('''
        INSERT INTO physical_answers (tg_id, name, course, "group", answer_13, answer_14, answer_15, answer_16,
         answer_17)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tg_id, name, course, group, answer_13, answer_14, answer_15, answer_16, answer_17))
    conn.commit()
    conn.close()


def save_daytime_answers(tg_id, name, course, group, answer_18, answer_19, answer_20, answer_21, answer_22):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('DELETE FROM daytime_answers WHERE tg_id = ?', (tg_id,))
    c.execute('''
        INSERT INTO daytime_answers (tg_id, name, course, "group", answer_18, answer_19, answer_20, answer_21,
         answer_22)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tg_id, name, course, group, answer_18, answer_19, answer_20, answer_21, answer_22))
    conn.commit()
    conn.close()


def save_psycho_answers(tg_id, name, course, group, answer_23, answer_24, answer_25, answer_26, answer_27, answer_28,
                        answer_29, answer_30):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('DELETE FROM psycho_answers WHERE tg_id = ?', (tg_id,))
    c.execute('''
        INSERT INTO psycho_answers (tg_id, name, course, "group", answer_23, answer_24, answer_25, answer_26, answer_27,
         answer_28, answer_29, answer_30)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tg_id, name, course, group, answer_23, answer_24, answer_25, answer_26, answer_27, answer_28, answer_29,
          answer_30))
    conn.commit()
    conn.close()


def pdf_report():
    filename = "Files pdf/Answers_Report.pdf"

    with open('TestQuestions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)

    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    survey_data = []

    table_info = {
        'food_answers': range(1, 7),
        'pain_answers': range(7, 13),
        'physical_answers': range(13, 18),
        'daytime_answers': range(18, 23),
        'psycho_answers': range(23, 31)
    }

    for table, question_range in table_info.items():
        for question_num in question_range:
            question_column = f'answer_{question_num}'
            question_text = questions.get(str(question_num), f"Вопрос {question_num}")
            try:
                c.execute(f"SELECT {question_column} FROM {table}")
                answers = c.fetchall()
            except:
                answers = []

            answer_counts = {}
            total_answers = len(answers)

            if total_answers == 0:
                survey_data.append((question_text, {"Нет ответов"}))
                continue

            for answer in answers:
                ans = answer[0]
                if ans:
                    answer_counts[ans] = answer_counts.get(ans, 0) + 1

            answer_percentages = {
                answer: f"{(count / total_answers) * 100:.2f}% ({count})"
                for answer, count in answer_counts.items()
            }

            survey_data.append((question_text, answer_percentages))

    conn.close()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('font', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('font', size=14)

    for question_text, answer_percentages in survey_data:
        pdf.multi_cell(0, 8, txt=f"{question_text}")
        pdf.set_font('font', size=12)
        for answer, percentage in answer_percentages.items():
            pdf.multi_cell(0, 6, txt=f"{answer} - {percentage}")
        pdf.ln(5)
        pdf.set_font('font', size=14)

    pdf.output(filename)


def pdf_report_course(course, group):
    with open('TestQuestions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)

    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    survey_data = []

    filters = []
    params = []

    if course != "all":
        filters.append("course = ?")
        params.append(course)

    if group != "all":
        filters.append('"group" = ?')
        params.append(group)

    where = "WHERE " + " AND ".join(filters) if filters else ""

    for question_num in range(1, 31):
        question_column = f'answer_{question_num}'
        question_text = questions.get(str(question_num), f"Вопрос {question_num}")

        query = f"SELECT {question_column} FROM answers {where}"
        c.execute(query, params)
        answers = c.fetchall()

        answer_counts = {}
        total_answers = len(answers)
        for answer in answers:
            answer = answer[0]
            answer_counts[answer] = answer_counts.get(answer, 0) + 1

        if total_answers > 0:
            answer_percentages = {
                answer: f"{(count / total_answers) * 100:.2f}% ({count})"
                for answer, count in answer_counts.items()
            }
        else:
            answer_percentages = {"Нет ответов": "0.00% (0)"}

        survey_data.append((question_text, answer_percentages))

    conn.close()

    course_label = str(course) if course != "all" else "all"
    group_label = group.replace("/", "_") if group != "all" else "all"

    filename = f"Files pdf/Statistic_{course_label}_{group_label}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('font', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('font', size=14)
    pdf.cell(200, 10, txt=f"Отчет по вопросам {course_label},  {group_label}", ln=True)

    for question_text, answer_percentages in survey_data:
        pdf.set_font('font', size=12)
        pdf.multi_cell(0, 8, txt=f"{question_text}")
        for answer, percentage in answer_percentages.items():
            pdf.multi_cell(0, 6, txt=f"  Ответ: {answer} - {percentage}")

        pdf.ln(2)

    pdf.output(filename)


def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=8))
    return password


def generate_users_pdf(group):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()

    if group.lower() == "all":
        c.execute('SELECT first_name, last_name, password, "group", course FROM users')
    else:
        c.execute('SELECT first_name, last_name, password, "group", course FROM users WHERE "group" = ?', (group,))

    students = c.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Bounded', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('Bounded', '', 12)
    pdf.cell(0, 10, txt="Список студентов", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font('Bounded', '', 12)
    pdf.cell(80, 10, "Логин", border=1, align="C")
    pdf.cell(35, 10, "Пароль", border=1, align="C")
    pdf.cell(50, 10, "Группа", border=1, align="C")
    pdf.cell(20, 10, "Курс", border=1, align="C")
    pdf.ln()
    for first_name, last_name, password, group_name, course in students:
        login = first_name + " " + last_name
        pdf.cell(80, 10, login, border=1)
        pdf.cell(35, 10, password, border=1)
        pdf.cell(50, 10, group_name, border=1)
        pdf.cell(20, 10, str(course), border=1)
        pdf.ln()

    pdf.output("Files pdf/users.pdf")


def generate_admins_pdf():
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('SELECT first_name, last_name, password FROM admins')
    admins = c.fetchall()
    conn.close()
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Bounded', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('Bounded', '', 12)
    pdf.cell(0, 10, txt="Список администраторов", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(100, 10, "Логин", border=1, align="C")
    pdf.cell(50, 10, "Пароль", border=1, align="C")
    pdf.ln()
    for first_name, last_name, password in admins:
        login = first_name + " " + last_name
        pdf.cell(100, 10, login, border=1)
        pdf.cell(50, 10, password, border=1)
        pdf.ln()

    pdf.output("Files pdf/admins.pdf")


def generate_statsmans_pdf():
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('SELECT first_name, last_name, password FROM statsmans')
    statsmans = c.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Bounded', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('Bounded', '', 12)
    pdf.cell(0, 10, txt="Список аналитиков", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(100, 10, "Логин", border=1, align="C")
    pdf.cell(50, 10, "Пароль", border=1, align="C")
    pdf.ln()
    for first_name, last_name, password in statsmans:
        login = f"{first_name} {last_name}"
        pdf.cell(100, 10, login, border=1)
        pdf.cell(50, 10, password, border=1)
        pdf.ln()

    pdf.output("Files pdf/statsmans.pdf")


def generate_illness_stats(years):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('SELECT ill_date FROM illnesses')
    dates = c.fetchall()
    conn.close()

    first_year = years.split(' - ')[0]
    second_year = years.split(' - ')[1]
    month_counts = {i: 0 for i in range(1, 11)}

    for d in dates:
        date = d[0]
        start_date = date.split(' - ')[0]
        day, month, year = start_date.split('.')
        if year == first_year and int(month) >= 9 or year == second_year and int(month) <= 6:
            month = int(month) + 4
            month_counts[month] += 1


    months = [
         "Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь"
    ]
    counts = [month_counts[m] for m in range(1, 11)]

    plt.figure(figsize=(10, 4))
    plt.plot(months, counts, marker='o')
    plt.xticks(months)
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    date = datetime.now().date()
    plt.savefig(f'Files png/illness_stats_{date}.png')
    plt.close()

    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.add_font('Bounded', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('Bounded', '', 12)
    pdf.cell(0, 5, txt=f"График заболеваний по месяцам {first_year} - {second_year}", ln=True, align="C")
    pdf.ln(2)
    pdf.image(f"Files png/illness_stats_{date}.png", x=-30)
    pdf.output(f'Files pdf/illness_stats{first_year}-{second_year}.pdf')


def generate_illness_stats_by_course(course, group, years):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()

    if group == "all":
        c.execute('SELECT ill_date FROM illnesses WHERE course = ?', (course,))
    else:
        c.execute('SELECT ill_date FROM illnesses WHERE course = ? AND "group" = ?', (course, group))

    dates = c.fetchall()
    conn.close()

    first_year = years.split(' - ')[0]
    second_year = years.split(' - ')[1]
    month_counts = {i: 0 for i in range(1, 11)}

    for d in dates:
        date = d[0]
        start_date = date.split(' - ')[0]
        day, month, year = start_date.split('.')
        if (year == first_year and int(month) >= 9) or (year == second_year and int(month) <= 6):
            month = int(month) + 4
            month_counts[month] += 1

    months = [
        "Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь"
    ]
    counts = [month_counts[m] for m in range(1, 11)]

    plt.figure(figsize=(10, 4))
    plt.plot(months, counts, marker='o')
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    date = datetime.now().date()

    group_name = group.replace("/", "_") if group != "all" else "all"
    image_path = f'Files png/illness_stats_course_{course}_{group_name}_{date}.png'
    plt.savefig(image_path)
    plt.close()

    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.add_font('Bounded', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('Bounded', '', 12)
    title = f"График заболеваний по месяцам ({course} курс, {group} группа, {first_year} - {second_year})"
    pdf.cell(0, 5, txt=title, ln=True, align="C")
    pdf.ln(2)
    pdf.image(image_path, x=-30)

    group_name = group.replace("/", "_") if group != "all" else "all"

    pdf.output(f'Files pdf/illness_stats_course_{course}_{group_name}_{first_year}-{second_year}.pdf')


def get_illness_ids(course, group, name, date_range):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()

    query = 'SELECT id, name, "group", course, ill_date FROM illnesses WHERE 1=1'
    params = []

    if str(course).lower() != "all":
        query += " AND course = ?"
        params.append(course)

    if str(group).lower() != "all":
        query += ' AND "group" = ?'
        params.append(group)

    if str(name).lower() != "all":
        query += " AND name = ?"
        params.append(name)

    c.execute(query, params)
    list = c.fetchall()
    conn.close()

    ids = []

    if " - " in date_range:
        start_str, end_str = date_range.split(" - ")
        start_date = datetime.strptime(start_str.strip(), "%d.%m.%Y").date()
        end_date = datetime.strptime(end_str.strip(), "%d.%m.%Y").date()
    else:
        single_date = datetime.strptime(date_range.strip(), "%d.%m.%Y").date()
        start_date = end_date = single_date

    for list_id, list_name, list_group, list_course, ill_date in list:
        first_date_str = ill_date.split(" - ")[0].strip()
        first_date = datetime.strptime(first_date_str, "%d.%m.%Y").date()
        if start_date <= first_date <= end_date:
            ids.append(list_id)
    return ids


def get_users(course, group):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()

    c.execute(
        '''SELECT first_name, last_name FROM users WHERE course = ? AND "group" = ?''',
        (course, group)
    )
    users = c.fetchall()
    conn.close()

    full_names = [f"{first} {last}" for first, last in users]
    return full_names


def add_message_db(name, tg_id, message_text):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()
    time_now = datetime.now().strftime("%d.%m %H.%M.%S  %Y")
    c.execute('''
        INSERT INTO messages (name, tg_id, message_text, time, answered)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, tg_id, message_text, time_now, "нет"))
    conn.commit()
    conn.close()


def get_message_ids_not_answered():
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('SELECT rowid FROM messages WHERE answered = "нет"')
    ids = [row[0] for row in c.fetchall()]
    conn.close()
    return ids


def get_message_names_by_ids(ids):
    where_in = ','.join('?' for _ in ids)
    query = f'''
            SELECT name, tg_id 
            FROM messages 
            WHERE rowid IN ({where_in})
        '''

    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute(query, ids)
    results = c.fetchall()
    conn.close()

    ids = set()
    names = []

    for name, tg_id in results:
        if tg_id not in ids:
            names.append(name)
            ids.add(tg_id)

    return names


def get_message_messages_by_name(name):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()

    c.execute("SELECT tg_id, message_text, time FROM messages WHERE name = ?", (name,))
    messages = c.fetchall()
    conn.close()

    if not messages:
        return []

    first_tg_id = messages[0][0]
    if all(row[0] == first_tg_id for row in messages):
        date_message = [f"({row[2]})\n{row[1]}" for row in messages]
        return first_tg_id, date_message
    else:
        return None, []


def add_reply(id_tg_user, id_tg_admin, answer, watched):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()

    c.execute('''
        INSERT INTO reply (id_tg_user, id_tg_admin, answer, watched)
        VALUES (?, ?, ?, ?)
    ''', (id_tg_user, id_tg_admin, answer, watched))

    conn.commit()
    conn.close()


def set_answered_messages(tg_id):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()

    c.execute('''
        UPDATE messages
        SET answered = 'yes'
        WHERE tg_id = ?
    ''', (tg_id,))

    conn.commit()
    conn.close()


def get_reply_no_watched(tg_id):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()

    c.execute('''
        SELECT answer
        FROM reply
        WHERE id_tg_user = ? AND watched = 'no'
    ''', (tg_id,))

    answers = [row[0] for row in c.fetchall()]

    c.execute('''
            UPDATE reply
            SET watched = 'yes'
            WHERE id_tg_user = ? AND watched = 'no'
        ''', (tg_id,))

    conn.commit()
    conn.close()
    return answers


def add_statsman(first_name, last_name, password):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO statsmans (first_name, last_name, password)
        VALUES (?, ?, ?)
    ''', (first_name, last_name, password))
    conn.commit()
    conn.close()


def check_statsman_in_db(first_name, last_name):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()
    c.execute('''
        SELECT * FROM statsmans WHERE first_name = ? AND last_name = ?
    ''', (first_name, last_name))
    result = c.fetchone()
    conn.close()
    return result is not None


def check_statsman_password(first_name, last_name, password):
    conn = sqlite3.connect("main_database.db")
    c = conn.cursor()
    c.execute('''
        SELECT password FROM statsmans WHERE first_name = ? AND last_name = ?
    ''', (first_name, last_name))
    result = c.fetchone()
    conn.close()
    return result and result[0] == password


if __name__ == "__main__":
    init_db()

pdf_report()