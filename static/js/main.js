// static/js/main.js

// Copy to clipboard function
function copyToClipboard(elementId) {
  const element = document.getElementById(elementId);
  if (!element) return;

  const text = element.value || element.textContent;

  // Use modern Clipboard API
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        showCopyFeedback(elementId);
      })
      .catch((err) => {
        console.error("Failed to copy:", err);
        fallbackCopy(text, elementId);
      });
  } else {
    // Fallback for older browsers
    fallbackCopy(text, elementId);
  }
}

function fallbackCopy(text, elementId) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();

  try {
    document.execCommand("copy");
    showCopyFeedback(elementId);
  } catch (err) {
    console.error("Fallback copy failed:", err);
  }

  document.body.removeChild(textarea);
}

function showCopyFeedback(elementId) {
  // Find the copy button for this element
  const element = document.getElementById(elementId);
  if (!element) return;

  const copyButton = element.parentElement.parentElement.querySelector(
    'button[onclick*="' + elementId + '"]'
  );
  if (!copyButton) return;

  const originalHTML = copyButton.innerHTML;
  copyButton.innerHTML = '<i class="bi bi-check"></i> Copied!';
  copyButton.classList.remove("btn-outline-primary");
  copyButton.classList.add("btn-success");

  setTimeout(() => {
    copyButton.innerHTML = originalHTML;
    copyButton.classList.remove("btn-success");
    copyButton.classList.add("btn-outline-primary");
  }, 2000);
}

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

  // All tasks: Dynamic form behavior
  setupTaskForms();
});

function setupTaskForms() {
  // Task 1, 2, 3 (simple file/text toggle)
  setupSimpleTaskForm("task1");
  setupSimpleTaskForm("task2");
  setupSimpleTaskForm("task3");

  // Task 4 & 5 (with encrypt/decrypt mode)
  setupTaskForm("task4");
  setupTaskForm("task5");
}

function setupSimpleTaskForm(taskId) {
  const form = document.getElementById(`${taskId}-form`);
  if (!form) return;

  const fileInputRadio = document.getElementById(`${taskId}-input-file`);
  const textInputRadio = document.getElementById(`${taskId}-input-text`);
  const fileSection = document.getElementById(`${taskId}-file-section`);
  const textSection = document.getElementById(`${taskId}-text-section`);
  const fileInput = document.getElementById(`${taskId}-file-input`);
  const textarea = document.getElementById(`${taskId}-text-input`);

  // Toggle file/text input sections
  function updateInputMethod() {
    const useFile = fileInputRadio && fileInputRadio.checked;
    if (fileSection) fileSection.style.display = useFile ? "" : "none";
    if (textSection) textSection.style.display = useFile ? "none" : "";

    // Clear the inactive input
    if (useFile && textarea) {
      textarea.value = "";
    } else if (!useFile && fileInput) {
      fileInput.value = "";
    }
  }

  // Event listeners
  if (fileInputRadio)
    fileInputRadio.addEventListener("change", updateInputMethod);
  if (textInputRadio)
    textInputRadio.addEventListener("change", updateInputMethod);

  // Initial state
  updateInputMethod();
}

function setupTaskForm(taskId) {
  const form = document.getElementById(`${taskId}-form`);
  if (!form) return;

  const encryptRadio = document.getElementById(`${taskId}-action-encrypt`);
  const decryptRadio = document.getElementById(`${taskId}-action-decrypt`);
  const fileInputRadio = document.getElementById(`${taskId}-input-file`);
  const textInputRadio = document.getElementById(`${taskId}-input-text`);
  const fileSection = document.getElementById(`${taskId}-file-section`);
  const textSection = document.getElementById(`${taskId}-text-section`);
  const fileInput = document.getElementById(`${taskId}-file-input`);
  const textarea = document.getElementById(`${taskId}-text-input`);

  // Hints
  const actionHint = document.getElementById(`${taskId}-action-hint`);
  const fileHint = document.getElementById(`${taskId}-file-hint`);
  const textHint = document.getElementById(`${taskId}-text-hint`);

  // Update action hints (encrypt/decrypt)
  function updateActionHints() {
    const isEncrypt = encryptRadio && encryptRadio.checked;

    if (actionHint) {
      actionHint.textContent = isEncrypt
        ? "Mã hóa dữ liệu bình thường thành hex"
        : "Giải mã chuỗi hex thành dữ liệu gốc";
    }

    if (fileHint) {
      fileHint.textContent = isEncrypt
        ? "File chứa dữ liệu plaintext cần mã hóa"
        : "File chứa ciphertext hex cần giải mã";
    }

    if (textHint) {
      textHint.textContent = isEncrypt
        ? "Nhập text bình thường để mã hóa"
        : "Paste chuỗi hex để giải mã";
    }

    if (textarea) {
      textarea.placeholder = isEncrypt
        ? "Nhập plaintext..."
        : "Paste hex ciphertext...";
    }
  }

  // Toggle file/text input sections
  function updateInputMethod() {
    const useFile = fileInputRadio && fileInputRadio.checked;
    if (fileSection) fileSection.style.display = useFile ? "" : "none";
    if (textSection) textSection.style.display = useFile ? "none" : "";

    // Clear the inactive input
    if (useFile && textarea) {
      textarea.value = "";
    } else if (!useFile && fileInput) {
      fileInput.value = "";
    }
  }

  // Event listeners
  if (encryptRadio) encryptRadio.addEventListener("change", updateActionHints);
  if (decryptRadio) decryptRadio.addEventListener("change", updateActionHints);
  if (fileInputRadio)
    fileInputRadio.addEventListener("change", updateInputMethod);
  if (textInputRadio)
    textInputRadio.addEventListener("change", updateInputMethod);

  // Initial state
  updateActionHints();
  updateInputMethod();

  // Auto-scroll to result after page load (if result exists)
  setupAutoScroll(taskId);
}

function setupAutoScroll(taskId) {
  // Check if there's a result on page load
  window.addEventListener("load", () => {
    const tabPane = document.getElementById(taskId);
    if (!tabPane) return;

    // Check if this tab is active and has results
    if (tabPane.classList.contains("show", "active")) {
      const hrElement = tabPane.querySelector("hr");
      if (hrElement) {
        setTimeout(() => {
          hrElement.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 300);
      }
    }
  });
}
