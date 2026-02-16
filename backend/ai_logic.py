import json
import os
from difflib import get_close_matches

DATA_FILE = "data.json"

def load_knowledge_base():
    """
    Loads the knowledge base from a JSON file.
    If the file doesn't exist, it creates an empty one.
    """
    # If using Render, we need to ensure the file path is correct relative to execution
    if not os.path.exists(DATA_FILE):
        return {"questions": []}
    
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_knowledge_base(data):
    """
    Saves the updated knowledge base back to the JSON file.
    """
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question, questions):
    """
    Uses Python's difflib to find a question in the database that 
    closely resembles the user's input.
    """
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question, knowledge_base):
    """
    Retrieves the answer associated with a specific question.
    """
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def respond(user_input):
    """
    Main function to generate a response.
    Returns a dict with 'answer' and a boolean 'found' to let the frontend know
    if it recognized the question.
    """
    knowledge_base = load_knowledge_base()
    best_match = find_best_match(user_input.lower(), [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return {"answer": answer, "found": True}
    else:
        return {"answer": "I don't know the answer. Can you teach me?", "found": False}

def learn(user_input, correct_answer):
    """
    Adds a new question-answer pair to the knowledge base.
    """
    knowledge_base = load_knowledge_base()
    
    # Add the new knowledge
    knowledge_base["questions"].append({"question": user_input.lower(), "answer": correct_answer})
    save_knowledge_base(knowledge_base)
    
    return {"status": "success", "message": "Thank you! I have learned something new."}
