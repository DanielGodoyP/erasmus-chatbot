import os
from flask import Flask, request, jsonify, render_template_string
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Interfaz HTML sencilla
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chatbot Erasmus La Salle</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        #chatbox { height: 300px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        #user-input { width: 80%; padding: 10px; }
        button { padding: 10px; }
    </style>
</head>
<body>
    <h2>Erasmus Chatbot 🤖</h2>
    <div id="chatbox"></div>
    <input type="text" id="user-input" placeholder="Pregúntame algo sobre Erasmus...">
    <button onclick="sendMessage()">Enviar</button>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatbox = document.getElementById('chatbox');
            if (!input.value) return;

            chatbox.innerHTML += `<p><b>Tú:</b> ${input.value}</p>`;
            
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: input.value})
            });
            const data = await response.json();
            
            chatbox.innerHTML += `<p><b>Bot:</b> ${data.response}</p>`;
            input.value = '';
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    prompt = f"Eres un asistente experto en el programa Erasmus de La Salle. Responde de forma amable y concisa: {user_message}"
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"response": completion.choices[0].message.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)