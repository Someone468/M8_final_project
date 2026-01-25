import sqlite3
from typing import Optional

def init_db():
    conn = sqlite3.connect('support_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            question TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_request(user_id: int, username: str, question: str, department: str):
    conn = sqlite3.connect('support_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_requests (user_id, username, question, department)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, question, department))
    conn.commit()
    conn.close()

FAQ = {
    "как оформить заказ": "Чтобы оформить заказ, перейдите в корзину и нажмите 'Оформить заказ'.",
    "не работает оплата": "Попробуйте обновить страницу или свяжитесь с отделом программистов.",
}

def get_answer(question: str) -> Optional[str]:
    return FAQ.get(question.lower(), None)

def add_faq(question: str, answer: str):
    FAQ[question.lower()] = answer
