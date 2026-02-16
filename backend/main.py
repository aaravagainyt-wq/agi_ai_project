from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import requests

app = FastAPI()

# ---------- Database ----------
conn = sqlite3.connect("memory.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS memory (
    question TEXT PRIMARY KEY,
    answer TEXT
)""")
conn.commit()

# ---------- Bad words ----------
BAD_WORDS = ["fuck","shit","bitch","asshole","dick","pussy","porn","sex","motherfucker"]

# ---------- Models ----------
class Chat(BaseModel):
    message: str

last_unknown = None

# ---------- Google Search ----------
def google_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        r = requests.get(url).json()
        return r.get("AbstractText")
    except:
        return None

# ---------- Chat Route ----------
@app.post("/chat")
def chat(data: Chat):
    global last_unknown
    msg = data.message.lower().strip()

    for bad in BAD_WORDS:
        if bad in msg:
            return {"reply":"I do not learn bad words."}

    c.execute("SELECT answer FROM memory WHERE question=?", (msg,))
    row = c.fetchone()

    if row:
        return {"reply":row[0]}

    if last_unknown:
        c.execute("INSERT OR REPLACE INTO memory VALUES (?,?)", (last_unknown, msg))
        conn.commit()
        last_unknown = None
        return {"reply":"Got it! I have learned this forever."}

    google = google_search(msg)
    if google:
        return {"reply":google}

    last_unknown = msg
    return {"reply":"I am a new AI! I do not know what to say to that! Please tell me what should I respond with!"}
