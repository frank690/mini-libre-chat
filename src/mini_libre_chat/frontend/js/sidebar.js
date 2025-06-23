import { loadChat } from "./chat.js";

async function fetchChatTitles() {
  try {
    const res = await fetch("/titles");
    if (!res.ok) throw new Error("Failed to fetch chat titles");

    const titles = await res.json();
    renderChatTitles(titles);
  } catch (err) {
    console.error("Error fetching chat titles:", err);
  }
}

function renderChatTitles(titles) {
  const list = document.getElementById("chat-titles");
  list.innerHTML = ""; // Clear existing

  for (const [id, title] of titles) {
    const li = document.createElement("li");
    li.textContent = title;
    li.dataset.chatId = id;
    li.classList.add("chat-title");

    li.addEventListener("click", () => {
      loadChat(id);
    });

    list.appendChild(li);
  }
}

function setupSidebarToggle() {
  const sidebar = document.getElementById("sidebar");
  const toggleBtnOutside = document.getElementById("toggle-btn-outside");
  const toggleBtnInside = document.getElementById("toggle-btn-inside");
  const main = document.getElementById("main");

  if (!sidebar || !toggleBtnOutside || !toggleBtnInside || !main) return;

  toggleBtnOutside.addEventListener("click", () => {
    sidebar.classList.add("open");
    main.classList.add("shifted");
  });

  toggleBtnInside.addEventListener("click", () => {
    sidebar.classList.remove("open");
    main.classList.remove("shifted");
  });
}

export { setupSidebarToggle, fetchChatTitles };
