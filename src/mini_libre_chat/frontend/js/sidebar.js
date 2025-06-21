export function setupSidebarToggle() {
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
