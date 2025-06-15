// welcome.js
const names = ["Foo", "Bar", "Baz"];
const nameElement = document.getElementById("name");
const welcome = document.getElementById("welcome-container");

let index = 0;

function rotateNames() {
  if (index >= names.length) return;
  nameElement.style.opacity = 0;

  setTimeout(() => {
    nameElement.textContent = names[index] + ".";
    nameElement.style.opacity = 1;
    index++;
    if (index < names.length) {
      setTimeout(rotateNames, 300);
    }
  }, 200);
}

function initWelcomeRotation() {
  setTimeout(rotateNames, 1000);
}

async function hideWelcome() {
  if (welcome && !welcome.classList.contains("hidden")) {
    welcome.classList.add("hidden");
    await new Promise(resolve => setTimeout(resolve, 300));
    welcome.style.display = "none";
  }
}

export { initWelcomeRotation, hideWelcome };
