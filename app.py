import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os 

# 1. Load the resume data
try:
    with open('resume_data.json', 'r') as f:
        RESUME_DATA = json.load(f)
except FileNotFoundError:
    print("Error: resume_data.json not found.")
    RESUME_DATA = {}

app = Flask(__name__)
CORS(app) 

# --- MOCK API Call Placeholder (FAKE AI) ---
def call_anthropic_api(prompt_text, resume_string):
    """MOCK FUNCTION: Returns a simple response based on keywords."""
    # Use Komali's name explicitly in the mock logic
    if "language" in prompt_text.lower() or "code" in prompt_text.lower():
        if "high school" in prompt_text.lower():
            return "Komali learned **Lua** in high school for making games. Currently, Komali is studying **C programming** and has prior experience with **Python**."
        else:
            return "Komali is currently learning **C programming** and is skilled in **Python Pandas** and **Lua**."
    elif "cloud" in prompt_text.lower() or "platform" in prompt_text.lower():
        return "Komali is actively learning and doing projects on three major platforms: **Amazon AWS, Microsoft Azure, and Google Cloud Vertex**."
    elif "education" in prompt_text.lower() or "vilnius" in prompt_text.lower():
        return "Komali is a **First-Year Student** at **Vilnius Tech**, studying **Bachelor's in Applied Artificial Intelligence**."
    elif "contact" in prompt_text.lower() or "email" in prompt_text.lower():
        return f"Komali's professional contact method is email at **{RESUME_DATA.get('contact', 'the listed email address')}**."
    elif "skill" in prompt_text.lower():
        return "Komali's skills include Data Analysis (Pandas), Cloud Computing Fundamentals (AWS/Azure/GCP), and Lua for game development."
    else:
        return "I am an AI assistant for Komali Sri Lakkoju. I have information on Komali's studies at Vilnius Tech (Applied AI), programming languages (C, Python, Lua), and cloud learning (AWS, Azure, GCP). How can I help?"
# ------------------------------------


@app.route('/ask', methods=['POST'])
def ask_chatbot():
    data = request.get_json()
    user_question = data.get('question', '')
    if not user_question:
        return jsonify({"answer": "Please provide a question."}), 400

    # 2. Format the resume data for the prompt
    resume_string = json.dumps(RESUME_DATA, indent=2)

    # 3. Construct the RAG Prompt (Updated to use Komali's name)
    SYSTEM_INSTRUCTION = (
        "You are a helpful, friendly, and professional assistant acting on behalf of the resume owner, **Komali Sri Lakkoju**. "
        "Your task is to answer the user's question by using ONLY the resume data provided below. "
        "If the answer is not in the data, politely state that you cannot answer based on the available information."
    )
    
    # We pass the question and data to the mock function
    ai_answer = call_anthropic_api(user_question, resume_string)

    # 4. Return the answer
    return jsonify({"answer": ai_answer})

if __name__ == '__main__':
    # Runs the Flask server on your computer at http://127.0.0.1:5000
    app.run(debug=True, port=5000)