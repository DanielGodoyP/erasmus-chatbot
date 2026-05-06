import os
from flask import Flask, request, jsonify, render_template_string
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- NUEVA FUNCIÓN: Esto es lo que lee tu archivo informacion.txt ---
def obtener_contexto():
    contexto = ""
    ruta_data = 'data'
    if os.path.exists(ruta_data):
        for archivo in os.listdir(ruta_data):
            # Lee cualquier archivo .txt en la carpeta data
            if archivo.endswith('.txt'):
                with open(os.path.join(ruta_data, archivo), 'r', encoding='utf-8') as f:
                    contexto += f.read() + "\n"
    return contexto[:4000] # Limitamos para que Groq no se sature
# -------------------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chatbot Erasmus La Salle</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .chat-container { width: 450px; background: white; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; }
        .header { background: #004a99; color: white; padding: 20px; text-align: center; font-weight: bold; font-size: 1.2em; }
        #chatbox { height: 400px; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; background: #fff; }
        .message { padding: 10px 15px; border-radius: 18px; max-width: 80%; font-size: 14px; line-height: 1.4; }
        .user { background: #004a99; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background: #e9ecef; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; }
        .input-area { border-top: 1px solid #eee; padding: 15px; display: flex; gap: 10px; background: white; }
        input { flex: 1; border: 1px solid #ddd; padding: 12px; border-radius: 25px; outline: none; }
        button { background: #004a99; color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; font-weight: bold; }
        button:hover { background: #003570; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">Erasmus La Salle 🤖</div>
        <div id="chatbox"></div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Escribe tu duda sobre Erasmus...">
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatbox = document.getElementById('chatbox');
            const msg = input.value;
            if (!msg) return;

            chatbox.innerHTML += `<div class="message user">${msg}</div>`;
            input.value = '';
            chatbox.scrollTop = chatbox.scrollHeight;

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            });
            const data = await response.json();
            chatbox.innerHTML += `<div class="message bot">${data.response}</div>`;
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
    
    # --- CAMBIO CLAVE: Aquí es donde el bot lee la información ---
    contexto = obtener_contexto() 
    
    prompt = f"""
    Eres el asistente oficial de movilidad del CSEU La Salle. 
    Usa estrictamente esta información de la convocatoria para responder:
    {contexto}
    
    Pregunta del alumno: {user_message}
    Respuesta amable y concisa:
    """
    # -------------------------------------------------------------
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"response": completion.choices[0].message.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)