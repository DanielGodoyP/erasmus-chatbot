(function () {
  // 1. Inyectar estilos CSS y fuente Montserrat
  const styleHTML = `
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    #lasalle-bot-container * {
        font-family: 'Montserrat', sans-serif !important;
        box-sizing: border-box;
    }

    /* Botón flotante principal */
    #chatbot-trigger {
        position: fixed; bottom: 20px; right: 20px; 
        width: 65px; height: 65px; 
        background-color: #1b2c65; 
        color: #ffc800;
        border-radius: 50%; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        cursor: pointer; z-index: 10000; 
        display: flex; justify-content: center; align-items: center;
        transition: all 0.3s ease;
        border: 2px solid #1b2c65;
    }
    
    /* Efecto Hover exacto de la guía de estilos */
    #chatbot-trigger:hover {
        background-color: #ffc800;
        color: #1b2c65;
        border: 2px solid #ffc800;
        transform: scale(1.05);
    }

    /* Ventana del Chat */
    #chatbot-box {
        display: none; 
        position: fixed; bottom: 95px; right: 20px; 
        width: 360px; background: white; 
        border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        z-index: 9999; overflow: hidden;
        border: 1px solid #e0e0e0;
    }

    /* Botones de acción y rápidos */
    .ls-btn {
        background-color: #ffc800;
        color: #1b2c65;
        border: 2px solid #ffc800;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Efecto Hover exacto de la guía de estilos */
    .ls-btn:hover {
        background-color: #1b2c65;
        color: #ffc800;
        border: 2px solid #1b2c65;
    }

    /* Scrollbar estilizada */
    #messages::-webkit-scrollbar { width: 6px; }
    #messages::-webkit-scrollbar-thumb { background: #1b2c65; border-radius: 3px; }
  </style>
  `;
  document.head.insertAdjacentHTML("beforeend", styleHTML);

  // 2. Estructura HTML del Chat
  const chatHTML = `
  <div id="lasalle-bot-container">
      <div id="chatbot-trigger" onclick="toggleChat()">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
      </div>

      <div id="chatbot-box">
        <div style="background:#1b2c65; color:white; padding:18px; font-weight:700; text-align:center; font-size: 16px; position:relative; border-bottom: 4px solid #e9b221;">
          <span style="display:flex; align-items:center; justify-content:center; gap:8px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffc800" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            Erasmus La Salle
          </span>
          <span onclick="toggleChat()" style="position:absolute; right:15px; top:18px; cursor:pointer; font-size:16px; opacity:0.8;">✖</span>
        </div>
        
        <div id="messages" style="height:350px; overflow-y:auto; padding:15px; background:#f4f7f6; display:flex; flex-direction:column; gap:12px;">
           <div style="text-align:left;">
             <span style="background:white; color:#1b2c65; padding:12px 16px; border-radius:15px 15px 15px 2px; border: 1px solid #e0e0e0; display:inline-block; font-size:14px; box-shadow:0 2px 4px rgba(0,0,0,0.05); font-weight: 500;">
               ¡Hola! Soy el asistente oficial de movilidad. ¿En qué te ayudo hoy?
             </span>
           </div>
        </div>

        <div style="padding: 10px 15px; display: flex; gap: 8px; overflow-x: auto; background: white; border-top: 1px solid #eee;">
            <button class="ls-btn" onclick="sendQuick('Plazos de solicitud')" style="font-size:12px; padding:6px 12px; border-radius:20px; white-space:nowrap;">📅 Plazos</button>
            <button class="ls-btn" onclick="sendQuick('Requisitos de idioma')" style="font-size:12px; padding:6px 12px; border-radius:20px; white-space:nowrap;">🗣️ Idiomas</button>
            <button class="ls-btn" onclick="sendQuick('Información de becas')" style="font-size:12px; padding:6px 12px; border-radius:20px; white-space:nowrap;">💶 Becas</button>
        </div>

        <div style="display:flex; border-top: 1px solid #eee; padding:10px 15px; background:white;">
          <input id="input" placeholder="Escribe tu duda..." style="flex:1; border:1px solid #ccc; padding:10px 15px; border-radius:25px; outline:none; font-size:14px; background:#f9f9f9;">
          
          <button class="ls-btn" onclick="sendMessage()" style="width:42px; height:42px; border-radius:50%; margin-left:10px; display:flex; justify-content:center; align-items:center; padding:0;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
          </button>
        </div>
      </div>
  </div>
  `;

  document.body.insertAdjacentHTML("beforeend", chatHTML);

  const box = document.getElementById("chatbot-box");
  const trigger = document.getElementById("chatbot-trigger");
  const input = document.getElementById("input");

  window.toggleChat = function() {
      if(box.style.display === "none" || box.style.display === "") {
          box.style.display = "block";
          trigger.style.transform = "scale(0)"; 
      } else {
          box.style.display = "none";
          trigger.style.transform = "scale(1)"; 
      }
  };

  window.sendQuick = function(texto) {
      input.value = texto;
      window.sendMessage();
  };

  input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      window.sendMessage();
    }
  });

  window.sendMessage = async function () {
    const msg = input.value.trim();
    if (!msg) return;

    const messagesDiv = document.getElementById("messages");
    
    // Burbuja del usuario (Fondo azul La Salle, texto amarillo)
    messagesDiv.innerHTML += `
      <div style="text-align:right;">
        <span style="background:#1b2c65; color:#ffc800; padding:12px 16px; border-radius:15px 15px 2px 15px; display:inline-block; font-size:14px; font-weight:600; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
          ${msg}
        </span>
      </div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    input.value = "";

    const typingId = "typing-" + Date.now();
    messagesDiv.innerHTML += `
      <div id="${typingId}" style="text-align:left;">
        <span style="background:white; color:#1b2c65; padding:12px 16px; border-radius:15px 15px 15px 2px; border: 1px solid #e0e0e0; display:inline-block; font-size:13px; font-style:italic;">
          Escribiendo...
        </span>
      </div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    try {
        // ⚠️ PON TU ENLACE DE RENDER AQUÍ (Ej: https://tu-proyecto.onrender.com/chat)
        const res = await fetch("https://erasmus-chatbot-lasalle.onrender.com/", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({message: msg})
        });

        const data = await res.json();
        document.getElementById(typingId).remove();
        
        // Burbuja del bot
        messagesDiv.innerHTML += `
          <div style="text-align:left;">
            <span style="background:white; color:#333; padding:12px 16px; border-radius:15px 15px 15px 2px; border: 1px solid #e0e0e0; border-left: 4px solid #e9b221; display:inline-block; font-size:14px; box-shadow:0 2px 4px rgba(0,0,0,0.05); line-height: 1.5;">
              ${data.response}
            </span>
          </div>`;
        messagesDiv.scrollTop = messagesDiv.scrollHeight; 

    } catch (error) {
        document.getElementById(typingId).remove();
        messagesDiv.innerHTML += `<div style="text-align:center;"><span style="color:red; font-size:12px; font-weight:bold;">Error de conexión.</span></div>`;
    }
  };
})();