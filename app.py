import os
from flask import Flask, request, jsonify, render_template_string
from groq import Groq
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def obtener_contexto():
    contexto = ""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_data = os.path.join(base_dir, 'data')
    
    if os.path.exists(ruta_data):
        for archivo in os.listdir(ruta_data):
            if archivo.endswith('.txt'):
                with open(os.path.join(ruta_data, archivo), 'r', encoding='utf-8') as f:
                    contexto += f.read() + "\n"
    
    contexto_recortado = contexto[:3000]
    
    print(f"DEBUG: Contexto limitado a {len(contexto_recortado)} caracteres")
    return contexto_recortado
# -----------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Movilidad Erasmus+ | La Salle</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: 'Montserrat', sans-serif; 
            margin: 0; 
            padding: 0; 
            background-color: #f8f9fa; 
            color: #333;
        }
        
        header {
            background-color: #ffffff;
            padding: 15px 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            border-bottom: 3px solid #ffc800; /* Línea amarilla corporativa */
        }
        
        .logo-lasalle {
            height: 45px;
        }

        .contenido {
            text-align: center;
            padding: 100px 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        
        h1 { 
            color: #1b2c65; /* Azul oficial */
            font-size: 2.8em; 
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        p.subtitulo { 
            font-size: 1.2em; 
            color: #555; 
            line-height: 1.6;
        }

        p.ayuda {
            font-size: 0.95em;
            color: #888;
            margin-top: 50px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <header>
        <img src="/static/logo.png" alt="Logo La Salle" class="logo-lasalle">
    </header>

    <div class="contenido">
        <h1>Movilidad Internacional</h1>
        <p class="subtitulo">
            Bienvenido al espacio de Programas Erasmus+ del CSEU La Salle.<br>
            Te acompañamos a donde quieras llegar: descubre destinos, becas y prepara tu próxima aventura académica.
        </p>
        
        <p class="ayuda">
            ¿Tienes alguna duda sobre plazos o requisitos de idioma?<br>
            Abre el asistente virtual en la esquina inferior derecha para obtener respuestas al instante.
        </p>
    </div>

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
        temperature=0.1  
    )
    return jsonify({"response": completion.choices[0].message.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)