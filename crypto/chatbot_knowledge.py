# crypto/chatbot_knowledge.py
"""
Knowledge base cho chatbot (offline) với nội dung tiếng Việt đầy đủ dấu.
Chỉ mô tả các mode được hỗ trợ trong code: ECB, CBC.
"""

KNOWLEDGE_BASE = {
    "caesar": {
        "description": "Caesar Cipher: mã hóa dịch chuyển mỗi chữ cái theo khóa k (0-25).",
        "algorithm": "Mã hóa: C = (P + K) mod 26\nGiải mã: P = (C - K) mod 26",
        "breaking": "Brute-force 26 khóa, chấm điểm bằng chi-square để chọn plaintext giống tiếng Anh nhất.",
        "implementation": "File: crypto/caesar.py, hàm: break_caesar(ciphertext)",
    },
    "substitution": {
        "description": "Monoalphabetic Substitution: ánh xạ A-Z -> A-Z một-đối-một (26!).",
        "breaking": "Hill-climb + random restart, score bằng quadgram + word bonus.",
        "implementation": "File: crypto/substitution.py, hàm: break_substitution(ciphertext)",
    },
    "vigenere": {
        "description": "Vigenère: dùng key lặp lại để shift nhiều Caesar.",
        "breaking": "Index of Coincidence ước lượng độ dài key, chi-square trên từng cột để tìm từng ký tự key.",
        "implementation": "File: crypto/vigenere.py, hàm: break_vigenere(ciphertext)",
        "ic_theory": "IC = ∑(fi(fi-1)) / (N(N-1)), IC ~0.065 cho tiếng Anh.",
    },
    "des": {
        "description": "DES: block 64-bit, key 56-bit, 16 round Feistel.",
        "implementation": "Files: crypto/des_core.py, crypto/des_modes.py, modes: ECB, CBC",
        "modes": "ECB: độc lập từng block; CBC: XOR với block trước, cần IV.",
    },
    "aes": {
        "description": "AES: block 128-bit, key 128/192/256-bit, cấu trúc SPN.",
        "implementation": "Files: crypto/aes_core.py, crypto/aes_modes.py, modes: ECB, CBC",
    },
    "modes": {
        "ecb": "ECB: đơn giản, không cần IV, nhưng lộ pattern nên không an toàn.",
        "cbc": "CBC: cần IV, che pattern tốt hơn ECB, mã hóa không song song.",
    },
    "project": {
        "features": "Tasks: Caesar, Substitution, Vigenère, DES (ECB/CBC), AES (ECB/CBC).",
    },
    "tasks": {
        "task1": "Task 1: Caesar Cipher Breaker (brute-force 26 khóa + chi-square).",
        "task2": "Task 2: Substitution Breaker (hill-climb + quadgram).",
        "task3": "Task 3: Vigenère Breaker (IC + chi-square).",
        "task4": "Task 4: DES Encrypt/Decrypt (ECB/CBC).",
        "task5": "Task 5: AES Encrypt/Decrypt (ECB/CBC, 128/192/256-bit).",
    },
}

# FAQ dùng để trả lời nhanh
FAQ = {
    "caesar": KNOWLEDGE_BASE["caesar"]["description"] + "\n\n" + KNOWLEDGE_BASE["caesar"]["algorithm"],
    "cách phá caesar": KNOWLEDGE_BASE["caesar"]["breaking"],
    "substitution": KNOWLEDGE_BASE["substitution"]["description"] + "\n\n" + KNOWLEDGE_BASE["substitution"]["breaking"],
    "vigenere": KNOWLEDGE_BASE["vigenere"]["description"] + "\n\n" + KNOWLEDGE_BASE["vigenere"]["breaking"],
    "des": KNOWLEDGE_BASE["des"]["description"] + "\n\n" + KNOWLEDGE_BASE["des"]["implementation"],
    "aes": KNOWLEDGE_BASE["aes"]["description"] + "\n\n" + KNOWLEDGE_BASE["aes"]["implementation"],
    "ecb": KNOWLEDGE_BASE["modes"]["ecb"],
    "cbc": KNOWLEDGE_BASE["modes"]["cbc"],
    "project": KNOWLEDGE_BASE["project"]["features"],
}

KEYWORDS = {
    "caesar": ["caesar", "shift"],
    "substitution": ["substitution", "monoalphabetic", "hill", "quadgram"],
    "vigenere": ["vigenere", "ic", "index of coincidence"],
    "des": ["des", "feistel"],
    "aes": ["aes", "rijndael"],
    "modes": ["ecb", "cbc", "mode", "iv"],
}


def find_best_match(query: str):
    q = query.lower()
    # exact-ish match
    for k, v in FAQ.items():
        if k in q:
            return v

    # keyword match
    best_topic = None
    best_score = 0
    for topic, kws in KEYWORDS.items():
        score = sum(1 for kw in kws if kw in q)
        if score > best_score:
            best_score = score
            best_topic = topic
    if best_topic:
        kb = KNOWLEDGE_BASE.get(best_topic, {})
        if "description" in kb:
            return kb["description"]
    return None


def get_response(user_message: str) -> str:
    """Trả lời tin nhắn bằng knowledge base offline."""
    msg = user_message.strip()
    if not msg:
        return "Vui lòng nhập nội dung câu hỏi."

    # chào hỏi
    greetings = ["hello", "hi", "chào", "xin chào", "hey"]
    if any(g in msg.lower() for g in greetings):
        return "Xin chào! Tôi là Crypto Assistant (offline). Tôi hỗ trợ: Caesar, Substitution, Vigenère, DES (ECB/CBC), AES (ECB/CBC)."

    answer = find_best_match(msg)
    if answer:
        return answer

    # Fallback: bắt đầu bằng '??' để backend biết tiếp tục thử Gemini nếu có
    return "?? Chưa có câu trả lời sẵn. Vui lòng hỏi cụ thể hơn về Caesar, Substitution, Vigenère, DES, AES hoặc mode ECB/CBC."
