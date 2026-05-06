from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from langchain_groq import ChatGroq 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

app = Flask(__name__)
CORS(app)

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# 1. BASE DE DATOS 
def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
    docs = []
    if not os.path.exists("data"): os.makedirs("data")
    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(f"data/{file}")
            docs.extend(loader.load())
    return FAISS.from_documents(docs, embeddings) if docs else None

db = get_vectorstore()

llm = ChatGroq(
    model_name="llama-3.1-8b-instant", 
    temperature=0.2
)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        if not db: return jsonify({"reply": "No hay PDFs en la carpeta data"})
        
        # Buscamos la info en el PDF
        docs = db.similarity_search(user_message, k=4)
        context = "\n\n".join([d.page_content for d in docs])
        
        # Preparamos la orden
        prompt = f"Responde en español usando este contexto:\n{context}\n\nPregunta: {user_message}"
        
        # Llamamos a Groq 
        response = llm.invoke(prompt)
        
        return jsonify({"reply": response.content})
        
    except Exception as e:
        print(f"🔥 Error: {e}") 
        return jsonify({"reply": "🔌 Vaya, parece que ha habido un fallo técnico. ¿Puedes volver a intentarlo?"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)