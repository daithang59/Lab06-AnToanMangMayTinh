// Chatbot functionality
class Chatbot {
  constructor() {
    this.container = null;
    this.messagesContainer = null;
    this.input = null;
    this.sendBtn = null;
    this.isOpen = false;
    this.isTyping = false;
    this.init();
  }

  init() {
    this.createChatbotHTML();
    this.attachEventListeners();
  }

  createChatbotHTML() {
    // Create chatbot toggle button
    const toggle = document.createElement("button");
    toggle.className = "chatbot-toggle";
    toggle.innerHTML = '<i class="bi bi-chat-dots-fill"></i>';
    toggle.id = "chatbot-toggle";
    document.body.appendChild(toggle);

    // Create chatbot container
    const container = document.createElement("div");
    container.className = "chatbot-container";
    container.id = "chatbot-container";
    container.innerHTML = `
      <div class="chatbot-header">
        <h5>
          <i class="bi bi-robot"></i>
          Crypto Assistant
        </h5>
        <button class="chatbot-close" id="chatbot-close">
          <i class="bi bi-x"></i>
        </button>
      </div>
      <div class="chatbot-messages" id="chatbot-messages">
        <div class="chat-welcome">
          <i class="bi bi-stars"></i>
          <h6>Welcome to Crypto Assistant!</h6>
          <p>Powered by Google Gemini 2.0 Flash</p>
          <div class="chat-suggestions">
            <button class="suggestion-chip" data-message="Explain how Caesar cipher works">
              🔤 Explain how Caesar cipher works
            </button>
            <button class="suggestion-chip" data-message="What is the difference between ECB and CBC mode?">
              🔐 What is ECB vs CBC mode?
            </button>
            <button class="suggestion-chip" data-message="How does AES encryption work?">
              🛡️ How does AES encryption work?
            </button>
            <button class="suggestion-chip" data-message="What is cryptanalysis?">
              🔍 What is cryptanalysis?
            </button>
          </div>
        </div>
      </div>
      <div class="chatbot-input-area">
        <textarea 
          class="chatbot-input" 
          id="chatbot-input" 
          placeholder="Ask me about cryptography..."
          rows="1"
        ></textarea>
        <button class="chatbot-send" id="chatbot-send">
          <i class="bi bi-send-fill"></i>
        </button>
      </div>
    `;
    document.body.appendChild(container);

    this.container = container;
    this.messagesContainer = container.querySelector("#chatbot-messages");
    this.input = container.querySelector("#chatbot-input");
    this.sendBtn = container.querySelector("#chatbot-send");
  }

  attachEventListeners() {
    const toggle = document.getElementById("chatbot-toggle");
    const close = document.getElementById("chatbot-close");

    toggle.addEventListener("click", () => this.toggleChat());
    close.addEventListener("click", () => this.toggleChat());

    this.sendBtn.addEventListener("click", () => this.sendMessage());
    this.input.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Auto-resize textarea
    this.input.addEventListener("input", () => {
      this.input.style.height = "auto";
      this.input.style.height = this.input.scrollHeight + "px";
    });

    // Suggestion chips
    this.messagesContainer.addEventListener("click", (e) => {
      const chip = e.target.closest(".suggestion-chip");
      if (chip) {
        const message = chip.dataset.message;
        this.input.value = message;
        this.sendMessage();
      }
    });
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
    const toggle = document.getElementById("chatbot-toggle");

    if (this.isOpen) {
      this.container.classList.add("show");
      toggle.classList.add("active");
      toggle.innerHTML = '<i class="bi bi-x-lg"></i>';
      this.input.focus();
    } else {
      this.container.classList.remove("show");
      toggle.classList.remove("active");
      toggle.innerHTML = '<i class="bi bi-chat-dots-fill"></i>';
    }
  }

  async sendMessage() {
    const message = this.input.value.trim();
    if (!message || this.isTyping) return;

    // Clear input
    this.input.value = "";
    this.input.style.height = "auto";

    // Remove welcome message if exists
    const welcome = this.messagesContainer.querySelector(".chat-welcome");
    if (welcome) welcome.remove();

    // Add user message
    this.addMessage(message, "user");

    // Show typing indicator
    this.showTyping();

    try {
      const response = await fetch("/api/chatbot", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      // Remove typing indicator
      this.hideTyping();

      if (data.success) {
        this.addMessage(data.response, "bot");
      } else {
        this.addMessage(
          `❌ Error: ${data.error}\n\nPlease make sure you have configured GEMINI_API_KEY in your .env file.`,
          "bot"
        );
      }
    } catch (error) {
      this.hideTyping();
      this.addMessage(
        `❌ Network error: ${error.message}\n\nPlease check your internet connection.`,
        "bot"
      );
    }
  }

  addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `chat-message ${sender}`;

    const avatar = document.createElement("div");
    avatar.className = "chat-avatar";
    avatar.innerHTML =
      sender === "user"
        ? '<i class="bi bi-person-fill"></i>'
        : '<i class="bi bi-robot"></i>';

    const bubble = document.createElement("div");
    bubble.className = "chat-bubble";

    // Format message with markdown-like syntax
    const formattedText = this.formatMessage(text);
    bubble.innerHTML = formattedText;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    this.messagesContainer.appendChild(messageDiv);
    this.scrollToBottom();
  }

  formatMessage(text) {
    // Basic markdown formatting
    let formatted = text
      // Code blocks
      .replace(/```(\w+)?\n([\s\S]*?)```/g, "<pre><code>$2</code></pre>")
      // Inline code
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      // Bold
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      // Italic
      .replace(/\*([^*]+)\*/g, "<em>$1</em>")
      // Line breaks
      .replace(/\n/g, "<br>");

    return formatted;
  }

  showTyping() {
    this.isTyping = true;
    this.sendBtn.disabled = true;

    const typingDiv = document.createElement("div");
    typingDiv.className = "chat-message bot";
    typingDiv.id = "typing-indicator";

    const avatar = document.createElement("div");
    avatar.className = "chat-avatar";
    avatar.innerHTML = '<i class="bi bi-robot"></i>';

    const bubble = document.createElement("div");
    bubble.className = "chat-bubble";
    bubble.innerHTML = `
      <div class="typing-indicator">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    `;

    typingDiv.appendChild(avatar);
    typingDiv.appendChild(bubble);

    this.messagesContainer.appendChild(typingDiv);
    this.scrollToBottom();
  }

  hideTyping() {
    this.isTyping = false;
    this.sendBtn.disabled = false;

    const typing = document.getElementById("typing-indicator");
    if (typing) typing.remove();
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }
}

// Initialize chatbot when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  new Chatbot();
});
