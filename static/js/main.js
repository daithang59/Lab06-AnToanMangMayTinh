// static/js/main.js

// ========================================
// TOAST NOTIFICATIONS
// ========================================
function showToast(message, type = "success", title = null) {
  const container =
    document.querySelector(".toast-container") || createToastContainer();

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;

  const icons = {
    success: "bi-check-circle-fill",
    error: "bi-x-circle-fill",
    warning: "bi-exclamation-triangle-fill",
    info: "bi-info-circle-fill",
  };

  const titles = {
    success: title || "Thành công",
    error: title || "Lỗi",
    warning: title || "Cảnh báo",
    info: title || "Thông báo",
  };

  toast.innerHTML = `
    <i class="toast-icon bi ${icons[type]}"></i>
    <div class="toast-content">
      <div class="toast-title">${titles[type]}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove()">×</button>
  `;

  container.appendChild(toast);

  // Animate in
  setTimeout(() => toast.classList.add("show"), 10);

  // Auto remove after 5 seconds
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 5000);

  // Click to dismiss
  toast.addEventListener("click", (e) => {
    if (!e.target.classList.contains("toast-close")) {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }
  });

  return toast;
}

function createToastContainer() {
  const container = document.createElement("div");
  container.className = "toast-container";
  document.body.appendChild(container);
  return container;
}

// ========================================
// LOADING OVERLAY
// ========================================
function showLoading(text = "Đang xử lý...", subtext = "Vui lòng đợi") {
  let overlay = document.querySelector(".loading-overlay");

  if (!overlay) {
    overlay = document.createElement("div");
    overlay.className = "loading-overlay";
    overlay.innerHTML = `
      <div class="loading-spinner">
        <div class="spinner"></div>
        <div class="loading-text">${text}</div>
        <div class="loading-subtext">${subtext}</div>
      </div>
    `;
    document.body.appendChild(overlay);
  }

  setTimeout(() => overlay.classList.add("show"), 10);
  return overlay;
}

function hideLoading() {
  const overlay = document.querySelector(".loading-overlay");
  if (overlay) {
    overlay.classList.remove("show");
    setTimeout(() => overlay.remove(), 300);
  }
}

// ========================================
// FILE VALIDATION
// ========================================
function validateFile(fileInput) {
  const file = fileInput.files[0];
  if (!file) return { valid: false, message: "" };

  const allowedExtensions = ["txt"];
  const maxSize = 10000; // 10000 characters

  // Check extension
  const fileName = file.name.toLowerCase();
  const extension = fileName.split(".").pop();

  if (!allowedExtensions.includes(extension)) {
    return {
      valid: false,
      message: `Chỉ chấp nhận file .txt (File hiện tại: .${extension})`,
    };
  }

  // Check size (approximate)
  const fileSizeInChars = file.size; // bytes ~ chars for text
  if (fileSizeInChars > maxSize) {
    return {
      valid: false,
      message: `File quá lớn. Tối đa ${maxSize} ký tự (File hiện tại: ~${fileSizeInChars} ký tự)`,
    };
  }

  return { valid: true, message: "File hợp lệ" };
}

function showFileValidation(fileInput, isValid, message) {
  const wrapper = fileInput.closest(".mb-3");
  if (!wrapper) return;

  // Remove old validation
  const oldIcon = wrapper.querySelector(".file-validation-icon");
  if (oldIcon) oldIcon.remove();

  const oldFeedback = wrapper.querySelector(".invalid-feedback");
  if (oldFeedback) oldFeedback.remove();

  if (!isValid) {
    // Show error
    fileInput.classList.add("is-invalid");
    const feedback = document.createElement("div");
    feedback.className = "invalid-feedback d-block";
    feedback.textContent = message;
    fileInput.parentElement.appendChild(feedback);

    showToast(message, "error", "File không hợp lệ");
  } else {
    fileInput.classList.remove("is-invalid");
    fileInput.classList.add("is-valid");

    setTimeout(() => {
      fileInput.classList.remove("is-valid");
    }, 2000);
  }
}

// ========================================
// CHARACTER COUNTER
// ========================================
function updateCharCounter(textarea) {
  const maxLength = 10000;
  const currentLength = textarea.value.length;
  const wrapper = textarea.closest(".mb-3");

  if (!wrapper) return;

  let counter = wrapper.querySelector(".char-counter");
  if (!counter) {
    counter = document.createElement("div");
    counter.className = "char-counter";
    textarea.parentElement.appendChild(counter);
  }

  counter.textContent = `${currentLength} / ${maxLength} ký tự`;

  // Update styling based on length
  counter.classList.remove("warning", "danger");

  if (currentLength > maxLength * 0.9) {
    counter.classList.add("danger");
  } else if (currentLength > maxLength * 0.7) {
    counter.classList.add("warning");
  }

  // Show toast if exceeded
  if (currentLength > maxLength) {
    textarea.classList.add("is-invalid");
    showToast(
      `Văn bản quá dài! Vui lòng rút ngắn xuống dưới ${maxLength} ký tự`,
      "error",
      "Vượt giới hạn"
    );
  } else {
    textarea.classList.remove("is-invalid");
  }
}

// ========================================
// DRAG & DROP FILE SUPPORT
// ========================================
function setupFileDragDrop(fileInput) {
  const wrapper = fileInput.closest(".mb-3");
  if (!wrapper || wrapper.querySelector(".drag-drop-overlay")) return;

  // Add drag overlay
  const overlay = document.createElement("div");
  overlay.className = "drag-drop-overlay";
  overlay.innerHTML =
    '<div class="drag-drop-text"><i class="bi bi-cloud-arrow-up"></i><br>Thả file vào đây</div>';
  wrapper.style.position = "relative";
  wrapper.appendChild(overlay);

  // Prevent default drag behaviors
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    wrapper.addEventListener(
      eventName,
      (e) => {
        e.preventDefault();
        e.stopPropagation();
      },
      false
    );
  });

  // Highlight on drag
  ["dragenter", "dragover"].forEach((eventName) => {
    wrapper.addEventListener(eventName, () => {
      overlay.classList.add("active");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    wrapper.addEventListener(eventName, () => {
      overlay.classList.remove("active");
    });
  });

  // Handle drop
  wrapper.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
      fileInput.files = files;

      // Trigger change event
      const event = new Event("change", { bubbles: true });
      fileInput.dispatchEvent(event);

      // Validate file
      const validation = validateFile(fileInput);
      showFileValidation(fileInput, validation.valid, validation.message);

      if (validation.valid) {
        showToast(`File "${files[0].name}" đã được chọn`, "success");
      }
    }
  });
}

// Copy to clipboard function with button feedback
function copyToClipboard(elementId, buttonElement = null) {
  const element = document.getElementById(elementId);
  if (!element) return;

  const text = element.value || element.textContent;

  // Use modern Clipboard API
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        showCopyFeedback(elementId, buttonElement);
      })
      .catch((err) => {
        console.error("Failed to copy:", err);
        fallbackCopy(text, elementId, buttonElement);
      });
  } else {
    // Fallback for older browsers
    fallbackCopy(text, elementId, buttonElement);
  }
}

function fallbackCopy(text, elementId, buttonElement = null) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();

  try {
    document.execCommand("copy");
    showCopyFeedback(elementId, buttonElement);
  } catch (err) {
    console.error("Fallback copy failed:", err);
  }

  document.body.removeChild(textarea);
}

function showCopyFeedback(elementId, buttonElement = null) {
  // Show toast notification
  showToast("Đã copy vào clipboard!", "success");

  // Use provided button or find it
  let copyButton = buttonElement;

  if (!copyButton) {
    const element = document.getElementById(elementId);
    if (element) {
      copyButton = element.parentElement.parentElement.querySelector(
        'button[onclick*="' + elementId + '"]'
      );
    }
  }

  if (!copyButton) return;

  const originalHTML = copyButton.innerHTML;
  const originalClasses = copyButton.className;

  copyButton.innerHTML = '<i class="bi bi-check-circle-fill"></i> Copied!';
  copyButton.classList.remove("btn-outline-primary", "btn-outline-secondary");
  copyButton.classList.add("btn-success");

  setTimeout(() => {
    copyButton.innerHTML = originalHTML;
    copyButton.className = originalClasses;
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

  // Setup AES key size selector
  setupAESKeySizeSelector();

  // Setup Key/IV validation for DES and AES
  setupKeyIVValidation();

  // Initialize Bootstrap tooltips
  const tooltipTriggerList = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]'
  );
  const tooltipList = [...tooltipTriggerList].map(
    (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
  );

  // Initial adjustments
  autoResizeTextareas();
  animateActiveCard();

  // ========================================
  // FILE INPUT VALIDATION
  // ========================================
  document
    .querySelectorAll('input[type="file"].form-control')
    .forEach((input) => {
      input.addEventListener("change", function () {
        if (this.files && this.files.length > 0) {
          const validation = validateFile(this);
          showFileValidation(this, validation.valid, validation.message);

          if (validation.valid) {
            this.classList.add("border-success");
            setTimeout(() => this.classList.remove("border-success"), 1500);
            showToast("File đã được chọn thành công", "success");
          }
        }
      });
    });

  // ========================================
  // TEXTAREA CHARACTER COUNTER
  // ========================================
  document.querySelectorAll("textarea.form-control").forEach((ta) => {
    // Auto-resize
    ta.addEventListener("input", function () {
      autoResizeTextareas();

      // Update character counter if it's a text input (not readonly)
      if (!this.readOnly) {
        updateCharCounter(this);
      }
    });

    // Initial counter setup for editable textareas
    if (!ta.readOnly && ta.value.length > 0) {
      updateCharCounter(ta);
    }
  });

  // ========================================
  // FORM SUBMISSION WITH LOADING
  // ========================================
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", function (e) {
      const submitBtn = this.querySelector('button[type="submit"]');
      if (!submitBtn) return;

      // Validate textareas
      const textareas = this.querySelectorAll("textarea:not([readonly])");
      let hasError = false;

      textareas.forEach((ta) => {
        if (ta.value.length > 10000) {
          e.preventDefault();
          hasError = true;
          showToast(
            "Vui lòng giảm độ dài văn bản xuống dưới 10,000 ký tự",
            "error",
            "Không thể submit"
          );
        }
      });

      if (hasError) return;

      // Show loading
      const taskName = this.id.replace("-form", "");
      const taskLabels = {
        task1: "Caesar Cipher",
        task2: "Substitution Cipher",
        task3: "Vigenère Cipher",
        task4: "DES Encryption",
        task5: "AES Encryption",
      };

      showLoading(
        `Đang xử lý ${taskLabels[taskName] || ""}...`,
        "Vui lòng đợi, quá trình này có thể mất vài giây"
      );

      // Add loading class to button
      submitBtn.classList.add("btn-loading");
    });
  });

  // All tasks: Dynamic form behavior
  setupTaskForms();

  // ========================================
  // AJAX FORM SUBMISSION (optional - for tasks 1-3)
  // ========================================
  setupAjaxForms();

  // ========================================
  // KEYBOARD SHORTCUTS
  // ========================================
  setupKeyboardShortcuts();
});

// ========================================
// KEYBOARD SHORTCUTS
// ========================================
function setupKeyboardShortcuts() {
  document.addEventListener("keydown", (e) => {
    // Ctrl/Cmd + Enter: Submit active form
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      const activePane = document.querySelector(".tab-pane.show.active");
      if (!activePane) return;

      const form = activePane.querySelector("form");
      if (form && !e.target.readOnly) {
        e.preventDefault();
        form.requestSubmit();
        showToast("Đang xử lý...", "info", "Keyboard Shortcut");
      }
    }

    // Ctrl/Cmd + C (when textarea focused): Copy
    if (
      (e.ctrlKey || e.metaKey) &&
      e.key === "c" &&
      e.target.tagName === "TEXTAREA" &&
      e.target.readOnly
    ) {
      // Default browser copy will work, just show toast
      setTimeout(() => {
        showToast("Đã copy vào clipboard", "success");
      }, 100);
    }

    // Escape: Hide loading
    if (e.key === "Escape") {
      const loadingOverlay = document.querySelector(".loading-overlay.show");
      if (loadingOverlay) {
        hideLoading();
        showToast("Đã hủy", "warning");
      }

      // Close toasts
      const toasts = document.querySelectorAll(".toast.show");
      toasts.forEach((toast) => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
      });
    }

    // Alt + 1-5: Switch tabs
    if (e.altKey && e.key >= "1" && e.key <= "5") {
      e.preventDefault();
      const tabIndex = parseInt(e.key) - 1;
      const tabs = document.querySelectorAll('[data-bs-toggle="pill"]');
      if (tabs[tabIndex]) {
        tabs[tabIndex].click();
        showToast(`Chuyển sang Task ${e.key}`, "info");
      }
    }

    // Ctrl/Cmd + K: Focus search/file input
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      const activePane = document.querySelector(".tab-pane.show.active");
      if (!activePane) return;

      const fileInput = activePane.querySelector('input[type="file"]');
      const textInput = activePane.querySelector("textarea:not([readonly])");

      if (textInput && textInput.offsetParent !== null) {
        textInput.focus();
      } else if (fileInput) {
        fileInput.click();
      }
    }
  });

  // Show keyboard shortcuts help on ?
  document.addEventListener("keydown", (e) => {
    if (e.key === "?" && !e.target.matches("input, textarea")) {
      e.preventDefault();
      showKeyboardHelp();
    }
  });

  // Show keyboard hint tooltip
  const keyboardHint = document.getElementById("keyboard-hint");
  if (keyboardHint) {
    setTimeout(() => {
      keyboardHint.classList.add("show");
      setTimeout(() => {
        keyboardHint.classList.remove("show");
      }, 5000);
    }, 1000);

    // Show on hover over form areas
    document.querySelectorAll(".card").forEach((card) => {
      card.addEventListener("mouseenter", () => {
        keyboardHint.classList.add("show");
      });
      card.addEventListener("mouseleave", () => {
        setTimeout(() => keyboardHint.classList.remove("show"), 2000);
      });
    });
  }
}

function showKeyboardHelp() {
  const shortcuts = [
    { keys: "Ctrl/Cmd + Enter", desc: "Submit form hiện tại" },
    { keys: "Ctrl/Cmd + K", desc: "Focus vào input" },
    { keys: "Alt + 1-5", desc: "Chuyển giữa các Task" },
    { keys: "Escape", desc: "Đóng loading/toast" },
    { keys: "?", desc: "Hiện trợ giúp này" },
  ];

  let html = '<div style="font-family: var(--font-body);">';
  html += '<h5 class="mb-3">⌨️ Keyboard Shortcuts</h5>';
  html += '<div style="display: grid; gap: 0.75rem;">';

  shortcuts.forEach((shortcut) => {
    html += `
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 1rem;">
        <kbd style="
          background: var(--code-bg);
          color: var(--text-main);
          padding: 0.25rem 0.5rem;
          border-radius: 0.25rem;
          font-family: monospace;
          border: 1px solid var(--code-border);
          font-size: 0.875rem;
          font-weight: 600;
        ">${shortcut.keys}</kbd>
        <span style="color: var(--text-main); font-size: 0.875rem; flex: 1;">${shortcut.desc}</span>
      </div>
    `;
  });

  html += "</div></div>";

  showToast(html, "info", "Keyboard Shortcuts");

  // Auto-close after 8 seconds
  setTimeout(() => {
    const toasts = document.querySelectorAll(".toast.show");
    if (toasts.length > 0) {
      toasts[toasts.length - 1].click();
    }
  }, 8000);
}

// ========================================
// AJAX FORM HANDLERS
// ========================================
function setupAjaxForms() {
  const ajaxTasks = ["task1", "task2", "task3"];

  ajaxTasks.forEach((taskId) => {
    const form = document.getElementById(`${taskId}-form`);
    if (!form) return;

    // Check if user wants AJAX (can be toggled)
    const useAjax = localStorage.getItem(`${taskId}_use_ajax`) !== "false";
    if (!useAjax) return;

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(this);
      const apiEndpoint = `/api/${taskId}/${getTaskAction(taskId)}`;

      // Show loading
      showLoading(`Đang xử lý ${getTaskName(taskId)}...`, "Vui lòng đợi");

      // Send AJAX request
      fetch(apiEndpoint, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          hideLoading();

          if (data.success) {
            // Show success toast
            showToast("Xử lý thành công!", "success");

            // Update UI with results
            displayResults(taskId, data);
          } else {
            // Show error toast
            showToast(data.error || "Có lỗi xảy ra", "error");

            // Display error in result area
            displayError(taskId, data.error);
          }
        })
        .catch((error) => {
          hideLoading();
          console.error("AJAX Error:", error);
          showToast("Lỗi kết nối. Vui lòng thử lại.", "error", "Lỗi");
        });
    });
  });
}

function getTaskAction(taskId) {
  const actions = {
    task1: "caesar",
    task2: "substitution",
    task3: "vigenere",
  };
  return actions[taskId] || "";
}

function getTaskName(taskId) {
  const names = {
    task1: "Caesar Cipher",
    task2: "Substitution Cipher",
    task3: "Vigenère Cipher",
  };
  return names[taskId] || "";
}

function displayResults(taskId, data) {
  const resultsSection = document.querySelector(`#${taskId} .card-body`);
  if (!resultsSection) return;

  // Remove old results
  let oldResults = resultsSection.querySelector(".ajax-results");
  if (oldResults) oldResults.remove();

  // Create results div
  const resultsDiv = document.createElement("div");
  resultsDiv.className = "ajax-results mt-4";

  let html = "<hr />";

  // Task-specific display
  if (taskId === "task1") {
    html += `
      <p><strong>Detected Key:</strong> ${data.key}</p>
      <div class="d-flex justify-content-between align-items-center mb-2">
        <label class="form-label fw-semibold mb-0">Plaintext:</label>
        <button type="button" class="btn btn-sm btn-outline-primary" onclick="copyResultText(this)">
          <i class="bi bi-clipboard"></i> Copy
        </button>
      </div>
      <textarea class="form-control" rows="10" readonly>${data.plaintext}</textarea>
    `;
  } else if (taskId === "task2") {
    html += `
      <p><strong>Score:</strong> ${data.score}</p>
      <p><strong>Mapping:</strong> ${data.mapping}</p>
      <div class="d-flex justify-content-between align-items-center mb-2">
        <label class="form-label fw-semibold mb-0">Plaintext:</label>
        <button type="button" class="btn btn-sm btn-outline-primary" onclick="copyResultText(this)">
          <i class="bi bi-clipboard"></i> Copy
        </button>
      </div>
      <textarea class="form-control" rows="10" readonly>${data.plaintext}</textarea>
    `;
  } else if (taskId === "task3") {
    html += `
      <p class="fw-semibold">
        <span class="text-primary">Recovered Key:</span>
        <span class="ms-2">${data.key}</span>
      </p>
      <div class="d-flex justify-content-between align-items-center mb-2">
        <label class="form-label fw-semibold mb-0">Plaintext:</label>
        <button type="button" class="btn btn-sm btn-outline-primary" onclick="copyResultText(this)">
          <i class="bi bi-clipboard"></i> Copy
        </button>
      </div>
      <textarea class="form-control" rows="10" readonly>${data.plaintext}</textarea>
    `;
  }

  resultsDiv.innerHTML = html;
  resultsSection.appendChild(resultsDiv);

  // Auto-resize textareas
  autoResizeTextareas();

  // Scroll to results
  setTimeout(() => {
    resultsDiv.scrollIntoView({ behavior: "smooth", block: "center" });
  }, 100);
}

function displayError(taskId, errorMessage) {
  const resultsSection = document.querySelector(`#${taskId} .card-body`);
  if (!resultsSection) return;

  // Remove old results
  let oldResults = resultsSection.querySelector(".ajax-results");
  if (oldResults) oldResults.remove();

  // Create error div
  const errorDiv = document.createElement("div");
  errorDiv.className = "ajax-results mt-4";
  errorDiv.innerHTML = `
    <hr />
    <div class="alert alert-danger" role="alert">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>
      <strong>Lỗi:</strong> ${errorMessage}
    </div>
  `;

  resultsSection.appendChild(errorDiv);

  // Scroll to error
  setTimeout(() => {
    errorDiv.scrollIntoView({ behavior: "smooth", block: "center" });
  }, 100);
}

// Copy result text from dynamically created textareas
function copyResultText(button) {
  const textarea = button.closest(".ajax-results").querySelector("textarea");
  if (!textarea) return;

  const text = textarea.value;

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        showCopySuccess(button);
      })
      .catch((err) => {
        console.error("Copy failed:", err);
      });
  } else {
    // Fallback
    textarea.select();
    document.execCommand("copy");
    showCopySuccess(button);
  }
}

function showCopySuccess(button) {
  const originalHTML = button.innerHTML;
  button.innerHTML = '<i class="bi bi-check"></i> Copied!';
  button.classList.remove("btn-outline-primary");
  button.classList.add("btn-success");

  setTimeout(() => {
    button.innerHTML = originalHTML;
    button.classList.remove("btn-success");
    button.classList.add("btn-outline-primary");
  }, 2000);
}

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

// ========================================
// AES KEY SIZE SELECTOR (Task 5)
// ========================================
function setupAESKeySizeSelector() {
  const keySizeSelect = document.getElementById("task5-key-size");
  const keyInput = document.getElementById("task5-key-input");
  const keyHint = document.getElementById("task5-key-hint");

  if (!keySizeSelect || !keyInput || !keyHint) return;

  function updateKeyPlaceholder() {
    const keySize = keySizeSelect.value;

    const configs = {
      128: {
        length: 32,
        bytes: 16,
        placeholder: "2B7E151628AED2A6ABF7158809CF4F3C",
        hint: "🔑 <strong>AES-128:</strong> 32 hex chars (16 bytes)",
      },
      192: {
        length: 48,
        bytes: 24,
        placeholder: "8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B",
        hint: "🔑 <strong>AES-192:</strong> 48 hex chars (24 bytes)",
      },
      256: {
        length: 64,
        bytes: 32,
        placeholder:
          "603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4",
        hint: "🔑 <strong>AES-256:</strong> 64 hex chars (32 bytes)",
      },
    };

    const config = configs[keySize];
    if (config) {
      keyInput.placeholder = config.placeholder;
      keyHint.innerHTML = config.hint;
    }
  }

  keySizeSelect.addEventListener("change", updateKeyPlaceholder);
  updateKeyPlaceholder(); // Initial update
}

// ========================================
// HEX KEY/IV VALIDATION (Client-side)
// ========================================
function validateHexInput(input, expectedLength, fieldName) {
  const value = input.value.replace(/\s/g, ""); // Remove whitespace
  const isValid = /^[0-9A-Fa-f]*$/.test(value);

  // Clear previous validation states
  input.classList.remove("is-valid", "is-invalid");

  // Remove existing feedback
  const existingFeedback =
    input.parentElement.querySelector(".invalid-feedback");
  if (existingFeedback) {
    existingFeedback.remove();
  }

  if (value.length === 0) {
    // Empty is okay (might be optional like IV)
    return true;
  }

  if (!isValid) {
    input.classList.add("is-invalid");
    const feedback = document.createElement("div");
    feedback.className = "invalid-feedback";
    feedback.textContent = `${fieldName} chỉ chấp nhận ký tự hex (0-9, A-F)`;
    input.parentElement.appendChild(feedback);
    return false;
  }

  if (expectedLength && value.length !== expectedLength) {
    input.classList.add("is-invalid");
    const feedback = document.createElement("div");
    feedback.className = "invalid-feedback";
    feedback.textContent = `${fieldName} phải có đúng ${expectedLength} ký tự hex (hiện tại: ${value.length})`;
    input.parentElement.appendChild(feedback);
    return false;
  }

  input.classList.add("is-valid");
  return true;
}

function setupKeyIVValidation() {
  // Task 4 - DES validation
  const task4Form = document.getElementById("task4-form");
  if (task4Form) {
    const keyInput = task4Form.querySelector('input[name="key"]');
    const ivInput = task4Form.querySelector('input[name="iv"]');

    if (keyInput) {
      keyInput.addEventListener("input", () => {
        validateHexInput(keyInput, 16, "DES Key");
      });
    }

    if (ivInput) {
      ivInput.addEventListener("input", () => {
        const value = ivInput.value.replace(/\s/g, "");
        if (value.length > 0) {
          validateHexInput(ivInput, 16, "DES IV");
        } else {
          ivInput.classList.remove("is-valid", "is-invalid");
          const feedback =
            ivInput.parentElement.querySelector(".invalid-feedback");
          if (feedback) feedback.remove();
        }
      });
    }

    // Form submission validation
    task4Form.addEventListener("submit", (e) => {
      let isValid = true;

      if (keyInput) {
        isValid = validateHexInput(keyInput, 16, "DES Key") && isValid;
      }

      const mode = task4Form.querySelector('select[name="mode"]').value;
      const action = task4Form.querySelector(
        'input[name="action"]:checked'
      ).value;

      if (mode === "CBC" && action === "decrypt" && ivInput) {
        isValid = validateHexInput(ivInput, 16, "DES IV") && isValid;
      }

      if (!isValid) {
        e.preventDefault();
        showToast("Vui lòng kiểm tra lại định dạng Key/IV", "error");
      }
    });
  }

  // Task 5 - AES validation
  const task5Form = document.getElementById("task5-form");
  if (task5Form) {
    const keySizeSelect = document.getElementById("task5-key-size");
    const keyInput = task5Form.querySelector('input[name="key"]');
    const ivInput = task5Form.querySelector('input[name="iv"]');

    if (keyInput && keySizeSelect) {
      keyInput.addEventListener("input", () => {
        const keySize = keySizeSelect.value;
        const expectedLength =
          keySize === "128" ? 32 : keySize === "192" ? 48 : 64;
        validateHexInput(keyInput, expectedLength, `AES-${keySize} Key`);
      });
    }

    if (ivInput) {
      ivInput.addEventListener("input", () => {
        const value = ivInput.value.replace(/\s/g, "");
        if (value.length > 0) {
          validateHexInput(ivInput, 32, "AES IV");
        } else {
          ivInput.classList.remove("is-valid", "is-invalid");
          const feedback =
            ivInput.parentElement.querySelector(".invalid-feedback");
          if (feedback) feedback.remove();
        }
      });
    }

    // Form submission validation
    task5Form.addEventListener("submit", (e) => {
      let isValid = true;

      if (keyInput && keySizeSelect) {
        const keySize = keySizeSelect.value;
        const expectedLength =
          keySize === "128" ? 32 : keySize === "192" ? 48 : 64;
        isValid =
          validateHexInput(keyInput, expectedLength, `AES-${keySize} Key`) &&
          isValid;
      }

      const mode = task5Form.querySelector('select[name="mode"]').value;
      const action = task5Form.querySelector(
        'input[name="action"]:checked'
      ).value;

      if (mode === "CBC" && action === "decrypt" && ivInput) {
        isValid = validateHexInput(ivInput, 32, "AES IV") && isValid;
      }

      if (!isValid) {
        e.preventDefault();
        showToast("Vui lòng kiểm tra lại định dạng Key/IV", "error");
      }
    });
  }
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
