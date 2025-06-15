// main.js
import { initTheme, setupThemeToggle } from './theme.js';
import { initWelcomeRotation, hideWelcome } from './welcome.js';
import { setupChat } from './chat.js';

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  setupThemeToggle();
  initWelcomeRotation();
  setupChat(hideWelcome);
});
