import { hideWelcome } from "./welcome.js";

const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const saveBtn = document.getElementById("save-btn");

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

  await hideWelcome(); // wait for welcome to hide

  appendMessage("user", userInput);
  input.value = "";

  appendMessage("assistant", "…");

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: userInput })
    });

    const data = await res.json();
    chat.lastChild.textContent = data.reply;
  } catch (err) {
    chat.lastChild.textContent = "⚠️ Error: Could not get response.";
    console.error(err);
  }
}

async function safe_chat() {
  const originalText = saveBtn.textContent;
  saveBtn.textContent = "Saving...";
  saveBtn.disabled = true;
  try {
    const res = await fetch("/save_chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    const data = await res.json();
    if (res.ok) {
      alert("✅ " + data.message);
    } else {
      alert("❌ " + (data.detail || "Save failed."));
    }
  } catch (err) {
    console.error("Save failed:", err);
    alert("⚠️ Could not save chat.");
  } finally {
    saveBtn.textContent = originalText;
    saveBtn.disabled = false;
  }
}

async function loadChat(chatId) {
  try {
    const res = await fetch(`/chat/${chatId}`);
    if (!res.ok) {
      throw new Error("Failed to load chat");
    }
    const chat = await res.json();
    await hideWelcome(); // in case loading was done on a virgin chat
    renderChat(chat);
  } catch (err) {
    console.error("Error loading chat:", err);
    alert("❌ Failed to load chat.");
  }
}

function renderChat(chat) {
  chat.innerHTML = ""; // Clear previous chat
  for (const message of chat.messages) {
    appendMessage(message.role, message.content);
  }
}

function setupChat() {
  sendBtn.addEventListener("click", () => sendMessage());
  saveBtn.addEventListener("click", () => safe_chat());
  input.addEventListener("keydown", e => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}

export { setupChat, loadChat };
