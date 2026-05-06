(function () {
  const chatHTML = `
  <div id="chatbot-box" style="
    position:fixed;
    bottom:20px;
    right:20px;
    width:300px;
    background:white;
    border-radius:10px;
    box-shadow:0 0 10px rgba(0,0,0,0.2);
    font-family:sans-serif;
  ">
    <div style="background:#003366;color:white;padding:10px;border-radius:10px 10px 0 0;">
      Erasmus Bot
    </div>
    <div id="messages" style="height:200px;overflow:auto;padding:10px;"></div>
    <div style="display:flex;">
      <input id="input" style="flex:1;border:none;padding:10px;">
      <button onclick="sendMessage()">➤</button>
    </div>
  </div>
  `;

  document.body.insertAdjacentHTML("beforeend", chatHTML);

  window.sendMessage = async function () {
    const input = document.getElementById("input");
    const msg = input.value;

    document.getElementById("messages").innerHTML += `<p><b>Tú:</b> ${msg}</p>`;

    const res = await fetch("https://TU_BACKEND.onrender.com/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: msg})
    });

    const data = await res.json();

    document.getElementById("messages").innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
    input.value = "";
  };
})();