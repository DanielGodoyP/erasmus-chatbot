(function () {
  const chatHTML = `
  <div id="chatbot-box" style="
    position:fixed;
    bottom:20px;
    right:20px;
    width:320px;
    background:white;
    border-radius:10px;
    box-shadow:0 0 15px rgba(0,0,0,0.2);
    font-family:sans-serif;
    z-index: 9999;
  ">
    <div style="background:#003366;color:white;padding:12px;border-radius:10px 10px 0 0; font-weight: bold; text-align: center;">
      Erasmus La Salle 🤖
    </div>
    
    <div id="messages" style="height:250px;overflow:auto;padding:10px; background:#f9f9f9;"></div>

    <div style="padding: 8px; display: flex; gap: 5px; overflow-x: auto; background: white; border-top: 1px solid #ddd;">
        <button onclick="sendQuick('Plazos')" style="font-size:12px; padding:5px 10px; border-radius:15px; border:1px solid #003366; background:white; color:#003366; cursor:pointer;">Plazos</button>
        <button onclick="sendQuick('Requisitos')" style="font-size:12px; padding:5px 10px; border-radius:15px; border:1px solid #003366; background:white; color:#003366; cursor:pointer;">Requisitos</button>
        <button onclick="sendQuick('Becas')" style="font-size:12px; padding:5px 10px; border-radius:15px; border:1px solid #003366; background:white; color:#003366; cursor:pointer;">Becas</button>
    </div>

    <div style="display:flex; border-top: 1px solid #ddd;">
      <input id="input" placeholder="Escribe tu duda..." style="flex:1;border:none;padding:12px; border-radius: 0 0 0 10px; outline:none;">
      <button onclick="sendMessage()" style="background:#003366; color:white; border:none; padding:10px 15px; border-radius: 0 0 10px 0; cursor:pointer;">➤</button>
    </div>
  </div>
  `;

  document.body.insertAdjacentHTML("beforeend", chatHTML);

  // Función para enviar al hacer clic en los botones rápidos
  window.sendQuick = function(texto) {
      document.getElementById("input").value = texto;
      window.sendMessage();
  };

  // Función principal para enviar mensajes
  window.sendMessage = async function () {
    const input = document.getElementById("input");
    const msg = input.value;
    if (!msg) return; // Si está vacío, no hace nada

    const messagesDiv = document.getElementById("messages");
    
    // Muestra el mensaje del usuario con estilo de "burbuja"
    messagesDiv.innerHTML += `<p style="margin:5px 0; text-align:right;"><b>Tú:</b> <span style="background:#003366; color:white; padding:5px 10px; border-radius:15px; display:inline-block;">${msg}</span></p>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll hacia abajo
    input.value = ""; // Limpia la caja de texto

    try {
        // Usamos ruta relativa '/chat' para que funcione en tu Render automáticamente
        const res = await fetch("/chat", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({message: msg})
        });

        const data = await res.json();

        // Muestra el mensaje del Bot. OJO: usamos data.response, no data.reply
        messagesDiv.innerHTML += `<p style="margin:5px 0; text-align:left;"><b>Bot:</b> <span style="background:#ddd; color:black; padding:5px 10px; border-radius:15px; display:inline-block;">${data.response}</span></p>`;
        messagesDiv.scrollTop = messagesDiv.scrollHeight; 

    } catch (error) {
        messagesDiv.innerHTML += `<p style="color:red; font-size:12px; text-align:center;">Error al conectar con el servidor.</p>`;
    }
  };
})();