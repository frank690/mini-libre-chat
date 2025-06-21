const toggle = document.getElementById("dark-mode-toggle");

function updateIcon() {
  const emoji = toggle.checked ? "🌑" : "☀️";
  const styleId = 'emoji-style';

  let styleTag = document.getElementById(styleId);
  if (!styleTag) {
    styleTag = document.createElement('style');
    styleTag.id = styleId;
    document.head.appendChild(styleTag);
  }

  styleTag.innerHTML = `.slider::before { content: "${emoji}"; }`;
}

function initTheme() {
  const saved = localStorage.getItem("theme");
  if (saved === "dark") {
    toggle.checked = true;
    document.body.classList.add("dark");
  } else {
    toggle.checked = false;
    document.body.classList.remove("dark");
  }
  updateIcon();
}

function setupThemeToggle() {
  toggle.addEventListener("change", () => {
    document.body.classList.toggle("dark", toggle.checked);
    localStorage.setItem("theme", toggle.checked ? "dark" : "light");
    updateIcon();
  });
}

export { initTheme, setupThemeToggle };
