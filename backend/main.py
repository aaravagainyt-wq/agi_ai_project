from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Import our logic
from ai_logic import respond, learn

app = FastAPI()

# --- CORS Configuration ---
# This allows your frontend (e.g., GitHub Pages) to send requests to this backend.
# In a strict production environment, replace ["*"] with your actual frontend URL.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class ChatRequest(BaseModel):
    user_input: str

class TeachRequest(BaseModel):
    user_input: str
    correct_answer: str

# --- Routes ---

@app.get("/")
def read_root():
    return {"message": "AI Chatbot Backend is Running!"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    Receives user input and returns the AI's best guess or a 'not found' message.
    """
    if not request.user_input:
        raise HTTPException(status_code=400, detail="Input cannot be empty")
    
    response = respond(request.user_input)
    return response

@app.post("/teach")
def teach_endpoint(request: TeachRequest):
    """
    Receives a question and the correct answer to store in the database.
    """
    if not request.user_input or not request.correct_answer:
        raise HTTPException(status_code=400, detail="Both input and answer are required")
    
    result = learn(request.user_input, request.correct_answer)
    return result

# --- Entry Point for Local Dev or Direct Execution ---
if __name__ == "__main__":
    # Render provides a PORT env var. Default to 8000 if not found.
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
