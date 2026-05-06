import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def home():
    return "Chatbot Erasmus funcionando (Modo Ligero)"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    # Prompt sencillo que simula el conocimiento del PDF
    prompt = f"Eres un asistente experto en el programa Erasmus de La Salle. Responde de forma amable: {user_message}"
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({"response": completion.choices[0].message.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)