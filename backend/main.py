from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from ai_logic import respond, learn

app = FastAPI()

# Initialize database
init_db()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str
    teach_answer: str | None = None   # optional auto-learning

@app.get("/")
def root():
    return {"message": "AI Chatbot Backend is Running!"}

@app.post("/chat")
def chat(request: ChatRequest):
    # AUTO LEARN: if user teaches during chat
    if request.teach_answer:
        learn(request.user_input, request.teach_answer)
        return {"answer": "Thanks — I learned that 🙂", "found": True}

    return respond(request.user_input)
