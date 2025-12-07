# crypto/chatbot_knowledge.py
"""
Knowledge Base cho Chatbot - Lab06 Cryptography
Chứa toàn bộ kiến thức về project để trả lời câu hỏi người dùng
"""

# Kiến thức về các thuật toán
KNOWLEDGE_BASE = {
    "caesar": {
        "description": "Caesar Cipher là mã hóa dịch chuyển (shift cipher) đơn giản nhất. Mỗi chữ cái được thay thế bằng chữ cái cách nó k vị trí trong bảng chữ cái.",
        "algorithm": "Mã hóa: C = (P + K) mod 26\nGiải mã: P = (C - K) mod 26",
        "example": "Với key=3: A→D, B→E, C→F, ... Z→C\nVí dụ: 'HELLO' → 'KHOOR'",
        "breaking": "Project sử dụng brute-force 26 khóa và đánh giá bằng chi-square statistic để tìm plaintext giống tiếng Anh nhất. Chi-square so sánh tần suất chữ cái với tần suất chuẩn tiếng Anh.",
        "implementation": "File: crypto/caesar.py\nHàm chính: break_caesar(ciphertext)\nTrả về: (key, plaintext, score)",
        "keyspace": "26 khóa có thể (0-25)",
    },
    "substitution": {
        "description": "Monoalphabetic Substitution Cipher thay thế mỗi chữ cái bằng một chữ cái khác theo một bảng ánh xạ cố định (26! khả năng).",
        "algorithm": "Mỗi chữ cái A-Z được ánh xạ 1-1 với một chữ cái khác. Ví dụ: A→Q, B→W, C→E, ...",
        "example": "Bảng ánh xạ: QWERTYUIOPASDFGHJKLZXCVBNM\n'HELLO' → 'ITSSG'",
        "breaking": "Sử dụng quadgram statistics + word dictionary + hill-climbing với random restart. Quadgram đánh giá mức độ giống tiếng Anh của 4 chữ cái liên tiếp. Random restart giúp thoát khỏi local maxima.",
        "implementation": "File: crypto/substitution.py\nHàm chính: break_substitution(ciphertext)\nData: english_quadgrams.txt (thống kê 4-gram), wordlist.txt\nTrả về: (score, mapping, plaintext)",
        "keyspace": "26! ≈ 4×10^26 khóa có thể (không thể brute-force)",
    },
    "vigenere": {
        "description": "Vigenère Cipher là polyalphabetic substitution sử dụng keyword. Mỗi chữ cái của key xác định một Caesar shift khác nhau.",
        "algorithm": "Mã hóa: Ci = (Pi + Ki mod L) mod 26\nGiải mã: Pi = (Ci - Ki mod L) mod 26\nTrong đó L là độ dài key",
        "example": "Key='CAT', Plaintext='HELLO'\nH+C=J, E+A=E, L+T=E, L+C=N, O+A=O → 'JEENO'",
        "breaking": "Bước 1: Dùng Index of Coincidence (IC) để ước lượng độ dài key. IC của tiếng Anh ≈ 0.065-0.068.\nBước 2: Chia ciphertext thành các nhóm theo vị trí key.\nBước 3: Giải mỗi nhóm như Caesar cipher bằng chi-square.\nBước 4: Chọn key cho plaintext tốt nhất.",
        "implementation": "File: crypto/vigenere.py\nHàm chính: break_vigenere(ciphertext)\nPhương pháp: IC analysis + frequency analysis\nTrả về: (key, plaintext, score)",
        "ic_theory": "IC = Σ(fi(fi-1))/(N(N-1)) trong đó fi là số lần xuất hiện chữ cái thứ i",
    },
    "des": {
        "description": "DES (Data Encryption Standard) là block cipher 64-bit với key 56-bit. Sử dụng 16 rounds Feistel network.",
        "algorithm": "Block size: 64 bits\nKey size: 56 bits (64 bits với parity)\n16 rounds với subkeys từ key schedule\nFeistel structure: L_{i+1} = R_i, R_{i+1} = L_i ⊕ F(R_i, K_i)",
        "implementation": "File: crypto/des_core.py, crypto/des_modes.py\nHàm: des_encrypt_block(), des_decrypt_block()\nModes: ECB, CBC, CTR",
        "modes": "ECB (Electronic Codebook): Mỗi block độc lập, không an toàn cho pattern.\nCBC (Cipher Block Chaining): Mỗi block XOR với ciphertext block trước, cần IV.\nCTR (Counter): Mã hóa counter và XOR với plaintext, có thể parallel.",
        "security": "DES key 56-bit đã bị coi là không an toàn (brute-force trong vài giờ). Thay thế bởi 3DES hoặc AES.",
    },
    "aes": {
        "description": "AES (Advanced Encryption Standard) là block cipher 128-bit với key 128/192/256-bit. Sử dụng Substitution-Permutation Network.",
        "algorithm": "Block size: 128 bits\nKey size: 128, 192, hoặc 256 bits\nRounds: 10 (AES-128), 12 (AES-192), 14 (AES-256)\nCác bước: SubBytes, ShiftRows, MixColumns, AddRoundKey",
        "implementation": "File: crypto/aes_core.py, crypto/aes_modes.py\nHàm: aes_encrypt_block(), aes_decrypt_block()\nHỗ trợ: AES-128, AES-192, AES-256\nModes: ECB, CBC, CTR",
        "security": "AES-128 an toàn cho hầu hết ứng dụng. AES-256 cho tính bảo mật cực cao. Hiện tại không có tấn công practical nào.",
        "sbox": "S-box: Bảng thay thế 16x16 phi tuyến, cung cấp confusion. Được tính từ inverse trong GF(2^8) và affine transform.",
    },
    "modes": {
        "ecb": "🔒 ECB (Electronic Codebook)\n\nChế độ mã hóa đơn giản nhất:\n\n✅ Ưu điểm:\n• Đơn giản, dễ implement\n• Có thể parallel hóa hoàn toàn\n• Không cần IV\n\n❌ Nhược điểm:\n• KHÔNG AN TOÀN: blocks giống nhau → ciphertext giống nhau\n• Lộ pattern của plaintext\n• Không nên dùng trong production\n\n💡 Cách hoạt động:\nMỗi block plaintext được mã hóa độc lập với cùng một key.",
        "cbc": "🔒 CBC (Cipher Block Chaining)\n\nChế độ phổ biến và an toàn:\n\n✅ Ưu điểm:\n• Mỗi block phụ thuộc block trước\n• An toàn hơn ECB nhiều\n• Che giấu pattern plaintext\n\n❌ Nhược điểm:\n• Cần IV (Initialization Vector) ngẫu nhiên\n• Không thể parallel encryption\n• Decrypt có thể parallel\n\n💡 Cách hoạt động:\nBlock i được XOR với ciphertext block (i-1) trước khi mã hóa.",
        "ctr": "🔒 CTR (Counter Mode)\n\nChế độ hiện đại, hiệu suất cao:\n\n✅ Ưu điểm:\n• Parallel hóa hoàn toàn (encrypt & decrypt)\n• Không cần padding\n• Chỉ cần encryption function\n• Random access blocks\n\n❌ Nhược điểm:\n• Cần nonce/counter duy nhất\n• Không được dùng lại nonce với cùng key\n\n💡 Cách hoạt động:\nMã hóa counter rồi XOR với plaintext.",
    },
    "project": {
        "structure": """
Cấu trúc project:
📦 Lab06_AnToanMangMayTinh/
├── 📁 crypto/          # Tất cả implementations tự viết
│   ├── caesar.py       # Caesar breaker với chi-square
│   ├── substitution.py # Substitution solver với quadgram
│   ├── vigenere.py     # Vigenère breaker với IC
│   ├── des_core.py     # DES implementation
│   ├── des_modes.py    # DES modes (ECB/CBC/CTR)
│   ├── aes_core.py     # AES implementation
│   └── aes_modes.py    # AES modes
├── 📁 data/            # Corpus và test files
├── 📁 static/          # CSS, JS, images
├── 📁 templates/       # HTML templates
├── app.py             # Flask backend
└── README.md          # Documentation
""",
        "features": "5 Tasks chính:\n1. Caesar Cipher Breaker\n2. Substitution Cipher Breaker\n3. Vigenère Cipher Breaker\n4. DES Encrypt/Decrypt (ECB, CBC, CTR)\n5. AES Encrypt/Decrypt (ECB, CBC, CTR, 128/192/256-bit)",
        "tech_stack": "Backend: Flask 3.0, Python 3.8+\nFrontend: Bootstrap 5.3, Vanilla JS\nCrypto: 100% tự implement (không dùng thư viện)",
    },
    
    "tasks": {
        "task1": "📝 Task 1: Caesar Cipher Breaker\n\nPhá mã Caesar cipher bằng brute-force 26 khóa và chấm điểm bằng chi-square statistic.\n\nInput: Ciphertext\nOutput: Key, plaintext, score\nFile: crypto/caesar.py",
        "task2": "📝 Task 2: Substitution Cipher Breaker\n\nPhá mã substitution cipher bằng hill-climbing với quadgram statistics và word dictionary.\n\nInput: Ciphertext\nOutput: Mapping, plaintext, score\nFile: crypto/substitution.py",
        "task3": "📝 Task 3: Vigenère Cipher Breaker\n\nPhá mã Vigenère bằng Index of Coincidence để tìm độ dài key, sau đó dùng frequency analysis.\n\nInput: Ciphertext\nOutput: Key, plaintext, score\nFile: crypto/vigenere.py",
        "task4": "📝 Task 4: DES Encryption/Decryption\n\nMã hóa và giải mã với DES (Data Encryption Standard):\n• Block size: 64 bits\n• Key size: 56 bits (16 hex chars)\n• Modes: ECB, CBC\n• Tự implement 100% Feistel network\n\nInput: Plaintext/Ciphertext, Key (hex), Mode\nOutput: Ciphertext/Plaintext (hex)\nFiles: crypto/des_core.py, crypto/des_modes.py",
        "task5": "📝 Task 5: AES Encryption/Decryption\n\nMã hóa và giải mã với AES (Advanced Encryption Standard):\n• Block size: 128 bits\n• Key size: 128/192/256 bits\n• Modes: ECB, CBC, CTR\n• Tự implement SubBytes, ShiftRows, MixColumns, AddRoundKey\n\nInput: Plaintext/Ciphertext, Key (hex), Mode\nOutput: Ciphertext/Plaintext (hex)\nFiles: crypto/aes_core.py, crypto/aes_modes.py",
    },
}

# Các câu hỏi thường gặp và câu trả lời
FAQ = {
    "caesar hoạt động thế nào": KNOWLEDGE_BASE["caesar"]["description"]
    + "\n\n"
    + KNOWLEDGE_BASE["caesar"]["algorithm"],
    "cách phá caesar": KNOWLEDGE_BASE["caesar"]["breaking"],
    "caesar example": KNOWLEDGE_BASE["caesar"]["example"],
    "substitution là gì": KNOWLEDGE_BASE["substitution"]["description"],
    "cách phá substitution": KNOWLEDGE_BASE["substitution"]["breaking"],
    "quadgram là gì": "Quadgram là chuỗi 4 chữ cái liên tiếp. Trong tiếng Anh, một số quadgram xuất hiện thường xuyên hơn (như 'TION', 'THER'). Quadgram statistics được dùng để đánh giá mức độ giống tiếng Anh của text.",
    "vigenere khác caesar": "Vigenère sử dụng nhiều Caesar shifts khác nhau (theo key), trong khi Caesar chỉ dùng 1 shift cố định. Vigenère an toàn hơn vì không có pattern tần suất đơn giản.",
    "index of coincidence": KNOWLEDGE_BASE["vigenere"]["ic_theory"]
    + "\nIC cao (~0.065) cho thấy text là monoalphabetic hoặc plaintext. IC thấp (~0.038) cho thấy polyalphabetic cipher.",
    "des vs aes": "DES: 56-bit key, 64-bit block, đã lỗi thời\nAES: 128/192/256-bit key, 128-bit block, chuẩn hiện tại\nAES nhanh hơn, an toàn hơn, và hỗ trợ key size lớn hơn.",
    "ecb là gì": KNOWLEDGE_BASE["modes"]["ecb"],
    "cbc là gì": KNOWLEDGE_BASE["modes"]["cbc"],
    "ctr là gì": KNOWLEDGE_BASE["modes"]["ctr"],
    "ecb": KNOWLEDGE_BASE["modes"]["ecb"],
    "cbc": KNOWLEDGE_BASE["modes"]["cbc"],
    "ctr": KNOWLEDGE_BASE["modes"]["ctr"],
    "ecb vs cbc vs ctr": KNOWLEDGE_BASE["modes"]["ecb"]
    + "\n\n"
    + KNOWLEDGE_BASE["modes"]["cbc"]
    + "\n\n"
    + KNOWLEDGE_BASE["modes"]["ctr"],
    "ecb vs cbc": KNOWLEDGE_BASE["modes"]["ecb"]
    + "\n\n"
    + KNOWLEDGE_BASE["modes"]["cbc"],
    "sự khác biệt ecb cbc": KNOWLEDGE_BASE["modes"]["ecb"]
    + "\n\n"
    + KNOWLEDGE_BASE["modes"]["cbc"],
    "project structure": KNOWLEDGE_BASE["project"]["structure"],
    "features": KNOWLEDGE_BASE["project"]["features"],
    "task 1": KNOWLEDGE_BASE["tasks"]["task1"],
    "task 2": KNOWLEDGE_BASE["tasks"]["task2"],
    "task 3": KNOWLEDGE_BASE["tasks"]["task3"],
    "task 4": KNOWLEDGE_BASE["tasks"]["task4"],
    "task 5": KNOWLEDGE_BASE["tasks"]["task5"],
    "nội dung task 1": KNOWLEDGE_BASE["tasks"]["task1"],
    "nội dung task 2": KNOWLEDGE_BASE["tasks"]["task2"],
    "nội dung task 3": KNOWLEDGE_BASE["tasks"]["task3"],
    "nội dung task 4": KNOWLEDGE_BASE["tasks"]["task4"],
    "nội dung task 5": KNOWLEDGE_BASE["tasks"]["task5"],
}

# Keywords mapping cho semantic search
KEYWORDS = {
    "caesar": ["caesar", "shift", "rot", "dịch chuyển", "brute force", "26"],
    "substitution": [
        "substitution",
        "monoalphabetic",
        "thay thế",
        "quadgram",
        "hill climbing",
    ],
    "vigenere": [
        "vigenere",
        "vigenère",
        "polyalphabetic",
        "keyword",
        "index of coincidence",
        "ic",
    ],
    "des": ["des", "data encryption standard", "feistel", "56 bit", "64 bit"],
    "aes": [
        "aes",
        "advanced encryption",
        "rijndael",
        "128",
        "192",
        "256",
        "sbox",
        "substitution permutation",
    ],
    "modes": ["ecb", "cbc", "ctr", "mode", "block", "iv", "initialization vector"],
    "breaking": ["break", "crack", "attack", "phá", "tấn công", "cryptanalysis"],
    "frequency": ["frequency", "tần suất", "chi square", "statistical"],
    "tasks": ["task", "task 1", "task 2", "task 3", "task 4", "task 5", "nhiệm vụ", "bài tập"],
}


def find_best_match(query: str) -> str:
    """
    Tìm kiến thức phù hợp nhất với query của user
    """
    query_lower = query.lower()

    # Exact match trong FAQ
    for question, answer in FAQ.items():
        if question in query_lower or query_lower in question:
            return answer

    # Keyword matching
    scores = {}
    for topic, keywords in KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            scores[topic] = score

    if scores:
        best_topic = max(scores, key=scores.get)
        kb = KNOWLEDGE_BASE.get(best_topic, {})

        # Xây dựng response từ knowledge base
        parts = []
        if "description" in kb:
            parts.append("📚 " + kb["description"])
        if "algorithm" in kb and any(
            w in query_lower
            for w in ["algorithm", "thuật toán", "công thức", "formula"]
        ):
            parts.append("\n🔢 Thuật toán:\n" + kb["algorithm"])
        if "example" in kb and any(
            w in query_lower for w in ["example", "ví dụ", "vd"]
        ):
            parts.append("\n� Ví dụ:\n" + kb["example"])
        if "breaking" in kb and any(
            w in query_lower for w in ["break", "crack", "phá", "giải", "attack"]
        ):
            parts.append("\n🔓 Cách phá:\n" + kb["breaking"])
        if "implementation" in kb and any(
            w in query_lower for w in ["implement", "code", "file", "triển khai"]
        ):
            parts.append("\n� Implementation:\n" + kb["implementation"])

        return "\n".join(parts) if parts else kb.get("description", "")

    return None


def get_response(user_message: str) -> str:
    """
    Trả lời câu hỏi của user dựa trên knowledge base
    """
    # Greetings
    greetings = ["hello", "hi", "chào", "xin chào", "hey"]
    if any(g in user_message.lower() for g in greetings):
        return "👋 Xin chào! Tôi là Crypto Assistant của Lab06.\n\nTôi có thể giúp bạn về:\n• Caesar Cipher\n• Substitution Cipher\n• Vigenère Cipher\n• DES & AES encryption\n• Block cipher modes (ECB, CBC, CTR)\n\nHãy hỏi tôi bất cứ điều gì! 🔐"

    # Help commands
    if any(h in user_message.lower() for h in ["help", "giúp", "hướng dẫn"]):
        return """🔐 **Lab06 Crypto Assistant - Hướng dẫn**

**Các chủ đề tôi có thể giúp:**
1️⃣ **Caesar Cipher** - Mã hóa dịch chuyển đơn giản
2️⃣ **Substitution** - Mã thay thế monoalphabetic
3️⃣ **Vigenère** - Mã polyalphabetic với keyword
4️⃣ **DES** - Data Encryption Standard (56-bit)
5️⃣ **AES** - Advanced Encryption Standard (128/192/256-bit)
6️⃣ **Block Cipher Modes** - ECB, CBC, CTR

**Ví dụ câu hỏi:**
• "Caesar cipher hoạt động thế nào?"
• "Cách phá Vigenère cipher?"
• "So sánh DES và AES"
• "Sự khác biệt giữa ECB và CBC?"
• "Quadgram là gì?"

Hãy thử hỏi tôi! 😊"""

    # Try to find answer
    answer = find_best_match(user_message)

    if answer:
        return answer

    # Fallback - general guidance
    return """🤔 Xin lỗi, tôi không hiểu câu hỏi này lắm.

**Tôi có thể trả lời các câu hỏi về:**
• **Caesar, Substitution, Vigenère ciphers** - Cách hoạt động và cách phá
• **DES, AES encryption** - Thuật toán và implementation
• **Block cipher modes** - ECB, CBC, CTR
• **Cryptanalysis techniques** - Frequency analysis, IC, quadgram

**Gợi ý:**
• Thử hỏi cụ thể hơn, ví dụ: "Caesar cipher là gì?"
• Hoặc gõ "help" để xem hướng dẫn đầy đủ

Hãy thử lại câu hỏi khác! 🔐"""
