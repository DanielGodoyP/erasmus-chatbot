import os
from flask import Flask, request, jsonify, render_template_string
from groq import Groq
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- FUNCIÓN CORREGIDA: Lectura segura de la carpeta data ---
def obtener_contexto():
    contexto = ""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_data = os.path.join(base_dir, 'data')
    
    if os.path.exists(ruta_data):
        for archivo in os.listdir(ruta_data):
            if archivo.endswith('.txt'):
                with open(os.path.join(ruta_data, archivo), 'r', encoding='utf-8') as f:
                    contexto += f.read() + "\n"
    
    # IMPORTANTE: Recortamos el texto a los primeros 3000 caracteres 
    # para no superar el límite de Groq (Error 413)
    contexto_recortado = contexto[:3000]
    
    print(f"DEBUG: Contexto limitado a {len(contexto_recortado)} caracteres")
    return contexto_recortado
# -----------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Campus Virtual La Salle</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            padding-top: 100px; 
            background-color: #f4f7f6; 
            color: #333;
        }
        h1 { color: #003366; font-size: 2.5em; }
        p { font-size: 1.2em; color: #666; }
    </style>
</head>
<body>
    <h1>🏛️ Portal de Alumnos - CSEU La Salle</h1>
    <p>Bienvenido al simulador de la página web de la universidad.</p>
    <p>Fíjate en la esquina inferior derecha de la pantalla 👇</p>

    <script src="/static/widget.js"></script>
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
    
    # Carga la información del archivo txt
    contexto = obtener_contexto() 
    
    # Prompt blindado para evitar alucinaciones (que la IA invente)
    prompt = f"""
    Eres el asistente oficial de movilidad del CSEU La Salle. 
    TU REGLA DE ORO: Responde ÚNICAMENTE basándote en el CONTEXTO proporcionado abajo. 
    Si la respuesta no está en el CONTEXTO, di: "Lo siento, no tengo esa información en las bases actuales".
    
    Al final de cada respuesta que des, añade obligatoriamente esta línea en cursiva:
    "Fuente: Bases de Convocatoria de Movilidad 26-27"

    CONTEXTO EXTRAÍDO DE LAS BASES:
    {contexto}
    
    PREGUNTA DEL ALUMNO: {user_message}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1  # Baja creatividad = mayor fidelidad al texto del archivo
    )
    return jsonify({"response": completion.choices[0].message.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)