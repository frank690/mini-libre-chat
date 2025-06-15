// chat.js
const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");

function appendMessage(role, text) {
  const msg = document.createElement("div");
  msg.classList.add("message", role);
  msg.textContent = text;
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage(hideWelcome) {
  const userInput = input.value.trim();
  if (!userInput) return;

  await hideWelcome(); // wait for welcome to hide

  appendMessage("user", userInput);
  input.value = "";

  appendMessage("assistant", "…");

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput })
    });

    const data = await res.json();
    chat.lastChild.textContent = data.reply;
  } catch (err) {
    chat.lastChild.textContent = "⚠️ Error: Could not get response.";
    console.error(err);
  }
}

function setupChat(hideWelcome) {
  sendBtn.addEventListener("click", () => sendMessage(hideWelcome));
  input.addEventListener("keydown", e => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(hideWelcome);
    }
  });
}

export { setupChat };
