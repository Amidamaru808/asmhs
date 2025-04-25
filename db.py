import sqlite3
import json
from fpdf import FPDF
import random
import string

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
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course TEXT,
            "group" TEXT,
            answer_1 TEXT,
            answer_2 TEXT,
            answer_3 TEXT,
            answer_4 TEXT,
            answer_5 TEXT,
            answer_6 TEXT,
            answer_7 TEXT,
            answer_8 TEXT,
            answer_9 TEXT,
            answer_10 TEXT,
            answer_11 TEXT,
            answer_12 TEXT,
            answer_13 TEXT,
            answer_14 TEXT,
            answer_15 TEXT,
            answer_16 TEXT,
            answer_17 TEXT,
            answer_18 TEXT,
            answer_19 TEXT,
            answer_20 TEXT,
            answer_21 TEXT,
            answer_22 TEXT,
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
    cursor = conn.cursor()
    cursor.execute('''
        SELECT password FROM admins WHERE first_name = ? AND last_name = ?
    ''', (first_name, last_name))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == password:
        return True
    else:
        return False


def load_questions(file_path='TestQuestions.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions

def fetch_all_answers():
    conn = sqlite3.connect('answers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM answers")
    all_answers = cursor.fetchall()
    conn.close()
    return all_answers


def save_answers(user_id, group, course, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7, answer_8,
                 answer_9, answer_10, answer_11, answer_12, answer_13, answer_14, answer_15, answer_16, answer_17,
                 answer_18, answer_19, answer_20, answer_21, answer_22, answer_23, answer_24, answer_25, answer_26,
                 answer_27, answer_28, answer_29, answer_30):
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    c.execute('''SELECT COUNT(*) FROM answers WHERE user_id = ?''', (user_id,))
    count = c.fetchone()[0]
    if count > 0:
        c.execute('''DELETE FROM answers WHERE user_id = ?''', (user_id,))
        conn.commit()

    c.execute(''' 
    INSERT INTO answers (
        user_id, "group", course, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7, answer_8,
        answer_9, answer_10, answer_11, answer_12, answer_13, answer_14, answer_15, answer_16, answer_17,
        answer_18, answer_19, answer_20, answer_21, answer_22, answer_23, answer_24, answer_25, answer_26,
        answer_27, answer_28, answer_29, answer_30
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, group, course, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7, answer_8,
        answer_9, answer_10, answer_11, answer_12, answer_13, answer_14, answer_15, answer_16, answer_17,
        answer_18, answer_19, answer_20, answer_21, answer_22, answer_23, answer_24, answer_25, answer_26,
        answer_27, answer_28, answer_29, answer_30
    ))
    conn.commit()
    conn.close()


def pdf_report():
    filename = "Answers_Report.pdf"
    with open('TestQuestions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)

    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    survey_data = []
    for question_num in range(1, 31):
        question_column = f'answer_{question_num}'

        question_text = questions.get(str(question_num), f"Вопрос {question_num}")
        c.execute(f"SELECT {question_column} FROM answers")
        answers = c.fetchall()
        answer_counts = {}
        total_answers = len(answers)

        if total_answers == 0:
            survey_data.append((question_text, {}))
            continue

        for answer in answers:
            answer = answer[0]
            answer_counts[answer] = answer_counts.get(answer, 0) + 1

        answer_percentages = {
            answer: f"{(count / total_answers) * 100:.2f}% ({count})" for answer, count in answer_counts.items()
        }

        survey_data.append((question_text, answer_percentages))

    conn.close()
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('font', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('font', size=14)

    for question_text, answer_percentages in survey_data:
        pdf.cell(200, 10, txt=f"{question_text}", ln=True)
        pdf.set_font('font', size=14)
        for answer, percentage in answer_percentages.items():
            pdf.cell(200, 5, txt=f"  Ответ: {answer} - {percentage}", ln=True)

    pdf.output(filename)
    print(f"pdf all: {filename}")


def pdf_report_course(course):
    with open('TestQuestions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    conn = sqlite3.connect('main_database.db')
    c = conn.cursor()
    survey_data = []
    for question_num in range(1, 31):
        question_column = f'answer_{question_num}'
        question_text = questions.get(str(question_num), f"Вопрос {question_num}")
        c.execute(f"SELECT {question_column} FROM answers WHERE course = ?", (course,))
        answers = c.fetchall()
        answer_counts = {}
        total_answers = len(answers)

        for answer in answers:
            answer = answer[0]
            answer_counts[answer] = answer_counts.get(answer, 0) + 1

        answer_percentages = {
            answer: f"{(count / total_answers) * 100:.2f}% ({count})" for answer, count in answer_counts.items()
        }

        survey_data.append((question_text, answer_percentages))
    filename = f"Statistic_{course}_course.pdf"
    conn.close()
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('font', '', 'Bounded-Regular.ttf', uni=True)
    pdf.set_font('font', size=14)
    pdf.cell(200, 10, txt=f"Отчет по вопросам для  {course} курса", ln=True)
    pdf.set_font('font', size=14)

    for question_text, answer_percentages in survey_data:
        pdf.cell(200, 10, txt=f"{question_text}", ln=True)

        for answer, percentage in answer_percentages.items():
            pdf.cell(200, 5, txt=f"  Ответ: {answer} - {percentage}", ln=True)

    pdf.output(filename)

    print(f"pdf course: {filename}")


def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=8))
    return password


if __name__ == "__main__":
    init_db()