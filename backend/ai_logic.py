import sqlite3
from difflib import get_close_matches

DB_NAME = "memory.db"

def get_all_questions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT question FROM knowledge")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def find_best_match(user_input):
    questions = get_all_questions()
    matches = get_close_matches(user_input.lower(), questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def respond(user_input):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    best_match = find_best_match(user_input)

    if best_match:
        cursor.execute(
            "SELECT answer FROM knowledge WHERE question=?",
            (best_match,)
        )
        result = cursor.fetchone()
        conn.close()

        return {"answer": result[0], "found": True}

    conn.close()
    return {"answer": "I don't know yet — teach me while chatting 🙂", "found": False}

def learn(user_input, correct_answer):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO knowledge (question, answer) VALUES (?, ?)",
        (user_input.lower(), correct_answer)
    )

    conn.commit()
    conn.close()

    return {"status": "learned"}
