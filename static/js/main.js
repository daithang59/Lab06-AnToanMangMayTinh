// static/js/main.js

// Helper: auto resize textarea height to fit content
function autoResizeTextareas() {
  document.querySelectorAll("textarea.form-control").forEach((ta) => {
    ta.style.height = "auto";
    ta.style.height = ta.scrollHeight + "px";
  });
}

// Helper: add appear animation to cards
function animateActiveCard() {
  const activePane = document.querySelector(".tab-pane.show.active");
  if (!activePane) return;
  const card = activePane.querySelector(".card");
  if (!card) return;

  card.classList.remove("appear");
  void card.offsetWidth; // force reflow
  card.classList.add("appear");
}

// Custom tab switching (không phụ thuộc Bootstrap JS)
function setupManualTabs() {
  const tabButtons = document.querySelectorAll('[data-bs-toggle="pill"]');
  const tabPanes = document.querySelectorAll(".tab-pane");

  tabButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();

      const targetSelector = btn.getAttribute("data-bs-target");
      if (!targetSelector) return;
      const targetPane = document.querySelector(targetSelector);
      if (!targetPane) return;

      // Xóa active khỏi tất cả buttons
      tabButtons.forEach((b) => b.classList.remove("active"));

      // Xóa show + active khỏi tất cả panes
      tabPanes.forEach((pane) => {
        pane.classList.remove("show");
        pane.classList.remove("active");
      });

      // Active button vừa click
      btn.classList.add("active");

      // Hiện pane tương ứng
      targetPane.classList.add("active");
      targetPane.classList.add("show");

      // Cuộn lên cho dễ nhìn
      targetPane.scrollIntoView({ behavior: "smooth", block: "start" });

      // Animation + resize textarea
      setTimeout(() => {
        autoResizeTextareas();
        animateActiveCard();
      }, 30);
    });
  });
}

// On document ready
document.addEventListener("DOMContentLoaded", () => {
  // Theme Toggle Logic
  const themeToggleBtn = document.getElementById("theme-toggle");
  const sunIcon = themeToggleBtn.querySelector(".sun-icon");
  const moonIcon = themeToggleBtn.querySelector(".moon-icon");
  const root = document.documentElement;

  // Check saved theme or system preference
  const savedTheme = localStorage.getItem("theme");
  const systemPrefersDark = window.matchMedia(
    "(prefers-color-scheme: dark)"
  ).matches;

  let currentTheme = savedTheme || (systemPrefersDark ? "dark" : "light");

  // Apply initial theme
  applyTheme(currentTheme);

  themeToggleBtn.addEventListener("click", () => {
    currentTheme = currentTheme === "light" ? "dark" : "light";
    applyTheme(currentTheme);
    localStorage.setItem("theme", currentTheme);
  });

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (theme === "dark") {
      sunIcon.style.display = "block";
      moonIcon.style.display = "none";
    } else {
      sunIcon.style.display = "none";
      moonIcon.style.display = "block";
    }
  }

  // Thiết lập tab thủ công
  setupManualTabs();

  // Initial adjustments
  autoResizeTextareas();
  animateActiveCard();

  // Khi file input đổi → highlight nhẹ
  document
    .querySelectorAll('input[type="file"].form-control')
    .forEach((input) => {
      input.addEventListener("change", () => {
        if (input.files && input.files.length > 0) {
          input.classList.add("border-success");
          setTimeout(() => input.classList.remove("border-success"), 1500);
        }
      });
    });

  // Re-auto-resize textarea khi nội dung đổi
  document.querySelectorAll("textarea.form-control").forEach((ta) => {
    ta.addEventListener("input", autoResizeTextareas);
  });
});
