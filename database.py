import sqlite3

conn = sqlite3.connect('edusmart.db')
cursor = conn.cursor()

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, review TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, direction INTEGER, level INTEGER, course TEXT)''')
    conn.commit()

def add_review(review):
    cursor.execute("INSERT INTO reviews (review) VALUES (?)", (review,))
    conn.commit()

def get_reviews():
    cursor.execute("SELECT review FROM reviews")
    return cursor.fetchall()

def add_enrollment(user_id, direction, level, course):
    cursor.execute("INSERT INTO enrollments (user_id, direction, level, course) VALUES (?, ?, ?, ?)", (user_id, direction, level, course))
    conn.commit()

def get_enrollments():
    cursor.execute("SELECT user_id, direction, level, course FROM enrollments")
    return cursor.fetchall()

create_table()
