import { initTheme, setupThemeToggle } from './theme.js';
import { initWelcomeRotation } from './welcome.js';
import { setupChat } from './chat.js';
import { setupSidebarToggle, fetchChatTitles } from './sidebar.js';

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  setupThemeToggle();
  initWelcomeRotation();
  setupChat();
  setupSidebarToggle();
  fetchChatTitles();
});
