const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const toggle = document.getElementById("dark-mode-toggle");

toggle.addEventListener("change", () => {
  document.body.classList.toggle("dark", toggle.checked);
  localStorage.setItem("theme", toggle.checked ? "dark" : "light");
});

window.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem("theme");
  if (saved === "dark") {
    toggle.checked = true;
    document.body.classList.add("dark");
  }
});

function appendMessage(role, text) {
  const msg = document.createElement("div");
  msg.classList.add("message", role);
  msg.textContent = text;
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
  const userInput = input.value.trim();
  if (!userInput) return;

  appendMessage("user", userInput);
  input.value = "";

  appendMessage("assistant", "…");

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: userInput})
    });

    const data = await res.json();
    chat.lastChild.textContent = data.reply;
  } catch (err) {
    chat.lastChild.textContent = "⚠️ Error: Could not get response.";
    console.error(err);
  }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
