# crypto/chatbot_knowledge.py
"""
Knowledge base cho chatbot (offline) với nội dung tiếng Việt đầy đủ dấu.
Chỉ mô tả các mode được hỗ trợ trong code: ECB, CBC.
Version: 2.0 - Cải thiện với nhiều thông tin chi tiết và ví dụ thực tế
"""

KNOWLEDGE_BASE = {
    "caesar": {
        "description": "Caesar Cipher là mã hóa thay thế đơn giản, dịch chuyển mỗi chữ cái trong bảng chữ cái theo một khóa k (0-25). Đây là một trong những phương pháp mã hóa cổ điển nhất.",
        "algorithm": "Mã hóa: C = (P + K) mod 26\nGiải mã: P = (C - K) mod 26\n\nVí dụ: Với K=3, 'HELLO' → 'KHOOR'",
        "breaking": "Phương pháp phá: Brute-force thử cả 26 khóa có thể (0-25), sau đó chấm điểm từng kết quả bằng chi-square test để tìm plaintext giống tiếng Anh nhất.\n\nĐộ phức tạp: O(26) - rất nhanh!",
        "implementation": "File: crypto/caesar.py\nHàm: break_caesar(ciphertext)\nĐầu vào: ciphertext (str)\nĐầu ra: (key, plaintext)",
        "security": "Độ bảo mật: RẤT YẾU - chỉ có 26 khóa có thể, dễ dàng bị phá bằng brute-force trong vài giây.",
        "example": "Input: 'KHOOR ZRUOG'\nKey tìm được: 3\nOutput: 'HELLO WORLD'",
    },
    "substitution": {
        "description": "Monoalphabetic Substitution Cipher: ánh xạ mỗi chữ cái sang một chữ cái khác theo bảng thay thế cố định (A→X, B→Y, ...). Có 26! ≈ 4×10²⁶ khóa có thể.",
        "breaking": "Phương pháp phá:\n1. Hill-climbing: bắt đầu từ mapping ngẫu nhiên, hoán đổi từng cặp ký tự để tăng điểm\n2. Random restart: thử nhiều điểm xuất phát khác nhau\n3. Scoring: Quadgram frequency (4-gram) + Word bonus (từ điển)\n\nQuadgram: đánh giá tần suất xuất hiện 4 chữ cái liên tiếp (VD: 'TION', 'THER')",
        "implementation": "File: crypto/substitution.py\nHàm: break_substitution(ciphertext)\nĐầu vào: ciphertext (str, ít nhất 500 ký tự khuyến nghị)\nĐầu ra: (score, mapping_str, plaintext)",
        "security": "Độ bảo mật: VỪA PHẢI - 26! khóa nhưng vẫn bị phá bằng frequency analysis hoặc hill-climbing.\nYêu cầu: văn bản đủ dài (>500 ký tự) mới phá hiệu quả.",
        "example": "Cipher alphabet: XFLNDAYQBZJOHSCTRGUVPEWIKM\nPlain alphabet:  ABCDEFGHIJKLMNOPQRSTUVWXYZ\n'HELLO' mã hóa thành 'ANJJQ'",
        "tips": "Mẹo phá thành công:\n- Văn bản càng dài càng chính xác\n- Chạy nhiều lần nếu kết quả chưa tốt\n- Điểm số (fitness score) càng cao càng tốt",
    },
    "vigenere": {
        "description": "Vigenère Cipher: mã hóa polyalphabetic sử dụng một key lặp lại để thực hiện nhiều phép Caesar khác nhau. Mỗi ký tự của key quyết định shift của ký tự tương ứng trong plaintext.",
        "algorithm": "Với key = 'KEY':\n- K → shift 10\n- E → shift 4\n- Y → shift 24\n\nLặp lại key cho toàn bộ plaintext: 'HELLO' + 'KEYKE' → 'RIJVS'",
        "breaking": "Phương pháp phá:\n1. Tính Index of Coincidence (IC) để ước lượng độ dài key\n2. Chia ciphertext thành các cột theo độ dài key\n3. Mỗi cột là một Caesar cipher → dùng chi-square test để tìm từng ký tự của key\n4. Ghép lại key hoàn chỉnh và giải mã",
        "implementation": "File: crypto/vigenere.py\nHàm: break_vigenere(ciphertext)\nĐầu vào: ciphertext (str)\nĐầu ra: (key, plaintext, score)",
        "ic_theory": "Index of Coincidence (IC):\nIC = Σ[fi(fi-1)] / [N(N-1)]\n\n- IC ≈ 0.065 cho tiếng Anh (văn bản thông thường)\n- IC ≈ 0.038 cho text ngẫu nhiên\n- IC giúp phát hiện độ dài key bằng cách tìm giá trị làm IC gần 0.065 nhất",
        "security": "Độ bảo mật: TRUNG BÌNH - an toàn hơn Caesar nhiều nhưng vẫn bị phá bằng Kasiski test hoặc IC analysis.\nYêu cầu: văn bản dài (>1000 ký tự) và key càng dài càng khó phá.",
        "example": "Plaintext: 'ATTACKATDAWN'\nKey: 'LEMON'\nCiphertext: 'LXFOPVEFRNHR'\n\nKey length tìm được: 5\nKey tìm được: 'LEMON'",
        "tips": "Mẹo phá thành công:\n- Văn bản càng dài càng dễ tìm key length\n- Key càng ngắn càng dễ phá\n- IC analysis đòi hỏi ít nhất 500-1000 ký tự",
    },
    "des": {
        "description": "DES (Data Encryption Standard): thuật toán mã hóa block cipher cổ điển, sử dụng:\n- Block size: 64-bit (8 bytes)\n- Key size: 56-bit (64-bit với 8 parity bit)\n- Cấu trúc: 16-round Feistel network\n- Đầu ra: ciphertext có độ dài bằng plaintext (sau padding)",
        "implementation": "Files:\n- crypto/des_core.py: Thuật toán DES core (permutation, S-box, F-function)\n- crypto/des_modes.py: Modes of operation (ECB, CBC)\n\nHàm chính:\n- des_encrypt(plaintext, key_hex, mode, iv_hex)\n- des_decrypt(ciphertext_hex, key_hex, mode, iv_hex)",
        "modes": "**ECB (Electronic Codebook):**\n- Mã hóa độc lập từng block\n- Không cần IV\n- ⚠️ Không an toàn: block giống nhau → ciphertext giống nhau\n\n**CBC (Cipher Block Chaining):**\n- XOR mỗi block plaintext với ciphertext block trước\n- Block đầu tiên XOR với IV (Initialization Vector)\n- ✓ An toàn hơn: che giấu pattern\n- IV phải random cho mỗi message",
        "security": "Độ bảo mật: YẾU (theo tiêu chuẩn hiện đại)\n- Key 56-bit đã bị phá bằng brute-force\n- Không nên dùng trong thực tế, chỉ để học tập\n- Thay thế: AES",
        "key_format": "Format khóa và IV:\n- Key: 16 ký tự hex (64-bit, trong đó 56-bit là key thực)\n- Ví dụ: '133457799BBCDFF1'\n- IV (cho CBC): 16 ký tự hex\n- Ví dụ: '0000000000000000'",
        "example": "Plaintext: 'Hello World!'\nKey: '133457799BBCDFF1'\nMode: CBC\nIV: '0000000000000000'\nCiphertext (hex): '8ca64de9c1b123a7'",
    },
    "aes": {
        "description": "AES (Advanced Encryption Standard): thuật toán mã hóa block cipher hiện đại, thay thế DES:\n- Block size: 128-bit (16 bytes)\n- Key size: 128-bit (10 rounds), 192-bit (12 rounds), hoặc 256-bit (14 rounds)\n- Cấu trúc: Substitution-Permutation Network (SPN)\n- Độ bảo mật: RẤT CAO - tiêu chuẩn mã hóa toàn cầu",
        "algorithm": "Mỗi round gồm 4 bước:\n1. SubBytes: thay thế byte qua S-box\n2. ShiftRows: dịch chuyển hàng\n3. MixColumns: trộn cột (trừ round cuối)\n4. AddRoundKey: XOR với round key",
        "implementation": "Files:\n- crypto/aes_core.py: Thuật toán AES core (S-box, MixColumns, key expansion)\n- crypto/aes_modes.py: Modes of operation (ECB, CBC)\n\nHàm chính:\n- aes_encrypt(plaintext, key_hex, mode, iv_hex, key_size)\n- aes_decrypt(ciphertext_hex, key_hex, mode, iv_hex, key_size)",
        "modes": "**ECB (Electronic Codebook):**\n- Giống DES-ECB: độc lập từng block\n- ⚠️ Không khuyến nghị: lộ pattern\n\n**CBC (Cipher Block Chaining):**\n- Giống DES-CBC: XOR với block trước\n- ✓ Khuyến nghị: an toàn hơn\n- Cần IV ngẫu nhiên 128-bit",
        "security": "Độ bảo mật: RẤT CAO\n- AES-128: 2¹²⁸ khóa có thể\n- AES-256: 2²⁵⁶ khóa có thể\n- Không thể brute-force với công nghệ hiện tại\n- Được chính phủ Mỹ chấp nhận cho tài liệu mật",
        "key_format": "Format khóa và IV:\n- AES-128: 32 ký tự hex (16 bytes)\n  Ví dụ: '2b7e151628aed2a6abf7158809cf4f3c'\n- AES-192: 48 ký tự hex (24 bytes)\n- AES-256: 64 ký tự hex (32 bytes)\n- IV: 32 ký tự hex (16 bytes)\n  Ví dụ: '000102030405060708090a0b0c0d0e0f'",
        "example": "Plaintext: 'Hello World!'\nKey (AES-128): '2b7e151628aed2a6abf7158809cf4f3c'\nMode: CBC\nIV: '000102030405060708090a0b0c0d0e0f'\nCiphertext (hex): '3ad77bb40d7a3660a89ecaf32466ef97'",
        "comparison": "So sánh AES vs DES:\n✓ AES an toàn hơn (128-256 bit vs 56 bit)\n✓ AES nhanh hơn trên phần cứng hiện đại\n✓ AES là tiêu chuẩn hiện tại (2001-nay)\n✗ DES đã lỗi thời (1977-2001)",
    },
    "modes": {
        "ecb": "**ECB (Electronic Codebook Mode):**\n\nCách hoạt động:\n- Chia plaintext thành các block\n- Mã hóa độc lập từng block bằng cùng key\n- C₁ = E(K, P₁), C₂ = E(K, P₂), ...\n\nƯu điểm:\n✓ Đơn giản, dễ implement\n✓ Không cần IV\n✓ Song song hóa được\n✓ Lỗi ở 1 block không ảnh hưởng block khác\n\nNhược điểm:\n✗ Block giống nhau → ciphertext giống nhau\n✗ Lộ pattern của plaintext (VD: ảnh ECB penguin)\n✗ Dễ bị known-plaintext attack\n✗ KHÔNG AN TOÀN cho hầu hết ứng dụng\n\nKhi nào dùng: Chỉ dùng để học tập, KHÔNG dùng trong thực tế!",
        "cbc": "**CBC (Cipher Block Chaining Mode):**\n\nCách hoạt động:\n- C₀ = IV (Initialization Vector)\n- C₁ = E(K, P₁ ⊕ IV)\n- C₂ = E(K, P₂ ⊕ C₁)\n- Cₙ = E(K, Pₙ ⊕ Cₙ₋₁)\n\nƯu điểm:\n✓ Che giấu pattern tốt\n✓ Block giống nhau → ciphertext khác nhau (do IV/previous block)\n✓ An toàn hơn ECB nhiều\n✓ Là mode phổ biến nhất\n\nNhược điểm:\n✗ Không song song hóa khi mã hóa\n✗ Lỗi ở 1 block ảnh hưởng block tiếp theo\n✗ Cần IV ngẫu nhiên cho mỗi message\n\nKhi nào dùng: Khuyến nghị cho hầu hết ứng dụng mã hóa dữ liệu!",
        "comparison": "So sánh ECB vs CBC:\n\n| Tiêu chí | ECB | CBC |\n|----------|-----|-----|\n| An toàn | ✗ Yếu | ✓ Tốt |\n| Cần IV | ✗ Không | ✓ Có |\n| Song song | ✓ Có | ✗ Không (encrypt) |\n| Pattern | ✗ Lộ | ✓ Che |\n| Sử dụng | Học tập | Thực tế |",
        "other_modes": "Các mode khác (không implement trong project này):\n- CTR (Counter): biến block cipher thành stream cipher\n- GCM (Galois/Counter): CBC + authentication\n- OFB, CFB: các biến thể khác",
    },
    "project": {
        "features": "Dự án Cryptography Lab bao gồm 5 Tasks:\n\nTask 1: Caesar Cipher Breaker\nTask 2: Substitution Cipher Breaker\nTask 3: Vigenère Cipher Breaker\nTask 4: DES Encrypt/Decrypt (ECB/CBC)\nTask 5: AES Encrypt/Decrypt (ECB/CBC, 128/192/256-bit)\n\n+ Chatbot AI hỗ trợ (Gemini API + offline knowledge base)",
        "structure": "Cấu trúc project:\n📁 crypto/\n  - caesar.py: Giải Caesar\n  - substitution.py: Giải Substitution\n  - vigenere.py: Giải Vigenère\n  - des_core.py, des_modes.py: DES\n  - aes_core.py, aes_modes.py: AES\n  - chatbot_knowledge.py: Knowledge base\n📁 data/: Dữ liệu (dictionary, n-gram frequencies)\n📁 templates/: HTML templates\n📁 static/: CSS, JS, images\n📄 app.py: Flask server chính",
    },
    "tasks": {
        "task1": "**Task 1: Caesar Cipher Breaker**\n\nMục tiêu: Phá mã Caesar tự động\n\nCách sử dụng:\n1. Upload file .txt hoặc nhập ciphertext\n2. Hệ thống tự động thử 26 khóa\n3. Chấm điểm bằng chi-square\n4. Trả về khóa và plaintext tốt nhất\n\nĐầu vào: Ciphertext (chỉ chữ cái A-Z)\nĐầu ra: Key (0-25), Plaintext\n\nFile: crypto/caesar.py",
        "task2": "**Task 2: Substitution Cipher Breaker**\n\nMục tiêu: Phá mã Substitution tự động\n\nCách sử dụng:\n1. Upload file .txt (khuyến nghị >1000 ký tự)\n2. Hệ thống dùng hill-climbing + random restart\n3. Scoring bằng quadgram + word bonus\n4. Trả về mapping và plaintext\n\nĐầu vào: Ciphertext (càng dài càng chính xác)\nĐầu ra: Score, Cipher alphabet, Plain alphabet, Plaintext\n\nTips: Chạy nhiều lần nếu kết quả chưa tốt!\n\nFile: crypto/substitution.py",
        "task3": "**Task 3: Vigenère Cipher Breaker**\n\nMục tiêu: Phá mã Vigenère tự động\n\nCách sử dụng:\n1. Upload file .txt (khuyến nghị >1000 ký tự)\n2. Hệ thống tính IC để tìm key length\n3. Chi-square test cho từng cột\n4. Ghép key và giải mã\n\nĐầu vào: Ciphertext (cần đủ dài)\nĐầu ra: Key, Plaintext, Score\n\nFile: crypto/vigenere.py",
        "task4": "**Task 4: DES Encrypt/Decrypt**\n\nMục tiêu: Mã hóa/giải mã DES\n\nCách sử dụng:\n1. Chọn Encrypt hoặc Decrypt\n2. Chọn mode: ECB hoặc CBC\n3. Nhập key (16 hex chars)\n4. Nhập IV nếu dùng CBC (16 hex chars)\n5. Nhập plaintext hoặc ciphertext\n\nĐầu ra: Hex ciphertext hoặc plaintext\n\nLưu ý: IV phải khác nhau cho mỗi message!\n\nFiles: crypto/des_core.py, crypto/des_modes.py",
        "task5": "**Task 5: AES Encrypt/Decrypt**\n\nMục tiêu: Mã hóa/giải mã AES\n\nCách sử dụng:\n1. Chọn Encrypt hoặc Decrypt\n2. Chọn key size: 128, 192, hoặc 256-bit\n3. Chọn mode: ECB hoặc CBC\n4. Nhập key (32/48/64 hex chars)\n5. Nhập IV nếu dùng CBC (32 hex chars)\n6. Nhập plaintext hoặc ciphertext\n\nĐầu ra: Hex ciphertext hoặc plaintext\n\nKhuyến nghị: AES-256 + CBC mode\n\nFiles: crypto/aes_core.py, crypto/aes_modes.py",
    },
    "security_best_practices": {
        "general": "Nguyên tắc bảo mật chung:\n\n1. KHÔNG dùng ECB mode trong thực tế\n2. LUÔN dùng IV ngẫu nhiên cho CBC\n3. Dùng AES thay vì DES\n4. Key phải được tạo ngẫu nhiên cryptographically secure\n5. Không hardcode key trong code\n6. Dùng authenticated encryption (GCM) nếu có thể",
        "key_management": "Quản lý khóa:\n\n- Sinh key: sử dụng os.urandom() hoặc secrets module\n- Lưu trữ: không lưu plaintext, dùng key derivation (PBKDF2, bcrypt)\n- Rotation: thay đổi key định kỳ\n- Backup: mã hóa key backup bằng key khác",
    },
    "common_errors": {
        "invalid_key": "Lỗi key không hợp lệ:\n- Kiểm tra độ dài key (DES: 16 hex, AES-128: 32 hex)\n- Key phải là hex characters (0-9, A-F)\n- Không có space hoặc ký tự đặc biệt",
        "invalid_iv": "Lỗi IV không hợp lệ:\n- CBC mode bắt buộc phải có IV\n- IV phải cùng độ dài với block size\n- DES: 16 hex chars, AES: 32 hex chars",
        "padding_error": "Lỗi padding:\n- Xảy ra khi decrypt với key sai\n- Hoặc ciphertext bị corrupt\n- Kiểm tra lại key và ciphertext",
    },
}

# FAQ dùng để trả lời nhanh - mở rộng với nhiều câu hỏi hơn
FAQ = {
    # Caesar Cipher
    "caesar": KNOWLEDGE_BASE["caesar"]["description"]
    + "\n\n"
    + KNOWLEDGE_BASE["caesar"]["algorithm"],
    "cách phá caesar": KNOWLEDGE_BASE["caesar"]["breaking"],
    "caesar là gì": KNOWLEDGE_BASE["caesar"]["description"],
    "caesar hoạt động như thế nào": KNOWLEDGE_BASE["caesar"]["algorithm"],
    "caesar an toàn không": KNOWLEDGE_BASE["caesar"]["security"],
    "ví dụ caesar": KNOWLEDGE_BASE["caesar"]["example"],
    # Substitution Cipher
    "substitution": KNOWLEDGE_BASE["substitution"]["description"]
    + "\n\n"
    + KNOWLEDGE_BASE["substitution"]["breaking"],
    "substitution là gì": KNOWLEDGE_BASE["substitution"]["description"],
    "cách phá substitution": KNOWLEDGE_BASE["substitution"]["breaking"],
    "substitution an toàn không": KNOWLEDGE_BASE["substitution"]["security"],
    "quadgram là gì": "Quadgram là chuỗi 4 chữ cái liên tiếp. Trong tiếng Anh, một số quadgram phổ biến: 'TION', 'THER', 'THAT', 'MENT'. Dùng để đánh giá xem văn bản có giống tiếng Anh tự nhiên không.",
    "hill climbing là gì": "Hill Climbing là thuật toán tối ưu hóa: bắt đầu từ một giải pháp, thử các thay đổi nhỏ, giữ lại thay đổi nào cải thiện được điểm số. Áp dụng trong phá substitution: hoán đổi các ký tự trong mapping để tăng điểm quadgram.",
    # Vigenere Cipher
    "vigenere": KNOWLEDGE_BASE["vigenere"]["description"]
    + "\n\n"
    + KNOWLEDGE_BASE["vigenere"]["breaking"],
    "vigenere là gì": KNOWLEDGE_BASE["vigenere"]["description"],
    "cách phá vigenere": KNOWLEDGE_BASE["vigenere"]["breaking"],
    "vigenere an toàn không": KNOWLEDGE_BASE["vigenere"]["security"],
    "index of coincidence": KNOWLEDGE_BASE["vigenere"]["ic_theory"]
    + "\n\nIC giúp phát hiện key length bằng cách đo độ tương đồng ký tự trong văn bản.",
    "ic là gì": KNOWLEDGE_BASE["vigenere"]["ic_theory"],
    "kasiski test": "Kasiski Test: phương pháp tìm key length bằng cách tìm các chuỗi lặp lại trong ciphertext. Khoảng cách giữa các lần lặp thường là bội số của key length.",
    # DES
    "des": KNOWLEDGE_BASE["des"]["description"]
    + "\n\n"
    + KNOWLEDGE_BASE["des"]["implementation"],
    "des là gì": KNOWLEDGE_BASE["des"]["description"],
    "des hoạt động như thế nào": KNOWLEDGE_BASE["des"]["description"],
    "des an toàn không": KNOWLEDGE_BASE["des"]["security"],
    "feistel là gì": "Feistel Network là cấu trúc mã hóa chia block thành 2 nửa (L, R), mỗi round: L'=R, R'=L⊕F(R,K). Ưu điểm: mã hóa và giải mã dùng cùng cấu trúc.",
    "s-box là gì": "S-box (Substitution box) là bảng tra cứu phi tuyến trong DES, biến 6 bit đầu vào thành 4 bit đầu ra. DES có 8 S-box, tạo tính confusion (làm rối mối quan hệ key-ciphertext).",
    "des key bao nhiêu bit": "DES dùng key 64-bit nhưng chỉ 56-bit thực sự được dùng (8 bit là parity). Format: 16 ký tự hex (ví dụ: '133457799BBCDFF1').",
    # AES
    "aes": KNOWLEDGE_BASE["aes"]["description"]
    + "\n\n"
    + KNOWLEDGE_BASE["aes"]["implementation"],
    "aes là gì": KNOWLEDGE_BASE["aes"]["description"],
    "aes hoạt động như thế nào": KNOWLEDGE_BASE["aes"]["algorithm"],
    "aes an toàn không": KNOWLEDGE_BASE["aes"]["security"],
    "aes vs des": KNOWLEDGE_BASE["aes"]["comparison"],
    "rijndael là gì": "Rijndael là tên gốc của AES, do hai nhà mật mã học Bỉ thiết kế (Joan Daemen và Vincent Rijmen). Năm 2001, NIST chọn Rijndael làm AES.",
    "aes key bao nhiêu bit": "AES hỗ trợ 3 kích thước key:\n- AES-128: 128-bit (32 hex chars) - 10 rounds\n- AES-192: 192-bit (48 hex chars) - 12 rounds\n- AES-256: 256-bit (64 hex chars) - 14 rounds",
    "subbytes là gì": "SubBytes là bước thay thế byte trong AES, mỗi byte đi qua S-box (bảng tra 16x16). Tạo tính non-linearity, chống cryptanalysis.",
    "mixcolumns là gì": "MixColumns là bước trộn cột trong AES, nhân ma trận 4x4 với mỗi cột của state. Tạo diffusion (lan tỏa ảnh hưởng của 1 bit input).",
    # Modes of Operation
    "ecb": KNOWLEDGE_BASE["modes"]["ecb"],
    "cbc": KNOWLEDGE_BASE["modes"]["cbc"],
    "ecb là gì": KNOWLEDGE_BASE["modes"]["ecb"],
    "cbc là gì": KNOWLEDGE_BASE["modes"]["cbc"],
    "ecb vs cbc": KNOWLEDGE_BASE["modes"]["comparison"],
    "mode nào an toàn": "CBC an toàn hơn ECB rất nhiều! ECB lộ pattern, không nên dùng trong thực tế. CBC che giấu pattern tốt, là mode phổ biến nhất.",
    "iv là gì": "IV (Initialization Vector) là block ngẫu nhiên dùng trong CBC mode để XOR với block plaintext đầu tiên. IV phải:\n- Ngẫu nhiên cho mỗi message\n- Cùng độ dài với block size (DES: 64-bit, AES: 128-bit)\n- Không cần bí mật, nhưng phải không đoán được",
    "tại sao ecb không an toàn": "ECB không an toàn vì:\n1. Block plaintext giống nhau → ciphertext giống nhau\n2. Lộ pattern của dữ liệu gốc (ví dụ: ảnh ECB penguin)\n3. Dễ bị cut-and-paste attack\n4. Không có diffusion giữa các block",
    "ctr mode": KNOWLEDGE_BASE["modes"]["other_modes"],
    "gcm mode": KNOWLEDGE_BASE["modes"]["other_modes"],
    # Project & Tasks
    "project": KNOWLEDGE_BASE["project"]["features"],
    "dự án này làm gì": KNOWLEDGE_BASE["project"]["features"],
    "có những task nào": KNOWLEDGE_BASE["project"]["features"],
    "cấu trúc project": KNOWLEDGE_BASE["project"]["structure"],
    "task 1": KNOWLEDGE_BASE["tasks"]["task1"],
    "task 2": KNOWLEDGE_BASE["tasks"]["task2"],
    "task 3": KNOWLEDGE_BASE["tasks"]["task3"],
    "task 4": KNOWLEDGE_BASE["tasks"]["task4"],
    "task 5": KNOWLEDGE_BASE["tasks"]["task5"],
    "hướng dẫn task 1": KNOWLEDGE_BASE["tasks"]["task1"],
    "hướng dẫn task 2": KNOWLEDGE_BASE["tasks"]["task2"],
    "hướng dẫn task 3": KNOWLEDGE_BASE["tasks"]["task3"],
    "hướng dẫn task 4": KNOWLEDGE_BASE["tasks"]["task4"],
    "hướng dẫn task 5": KNOWLEDGE_BASE["tasks"]["task5"],
    # Security & Best Practices
    "best practices": KNOWLEDGE_BASE["security_best_practices"]["general"],
    "nguyên tắc bảo mật": KNOWLEDGE_BASE["security_best_practices"]["general"],
    "quản lý key": KNOWLEDGE_BASE["security_best_practices"]["key_management"],
    "cách tạo key an toàn": KNOWLEDGE_BASE["security_best_practices"]["key_management"],
    # Common Errors
    "lỗi key": KNOWLEDGE_BASE["common_errors"]["invalid_key"],
    "lỗi iv": KNOWLEDGE_BASE["common_errors"]["invalid_iv"],
    "lỗi padding": KNOWLEDGE_BASE["common_errors"]["padding_error"],
    "key không hợp lệ": KNOWLEDGE_BASE["common_errors"]["invalid_key"],
    "iv không hợp lệ": KNOWLEDGE_BASE["common_errors"]["invalid_iv"],
    # General Crypto Concepts
    "mã hóa là gì": "Mã hóa (Encryption) là quá trình biến đổi dữ liệu plaintext thành ciphertext không đọc được, chỉ có người có key mới giải mã được. Mục đích: bảo vệ tính bí mật (confidentiality).",
    "plaintext là gì": "Plaintext là dữ liệu gốc, chưa mã hóa, có thể đọc được.",
    "ciphertext là gì": "Ciphertext là dữ liệu đã mã hóa, không đọc được nếu không có key.",
    "key là gì": "Key (khóa) là thông tin bí mật dùng để mã hóa và giải mã. Độ an toàn của hệ mã phụ thuộc vào key, không phụ thuộc vào thuật toán.",
    "symmetric encryption": "Symmetric Encryption (mã hóa đối xứng) dùng CÙNG KEY cho cả mã hóa và giải mã. Ví dụ: AES, DES, Caesar. Ưu điểm: nhanh. Nhược điểm: phải chia sẻ key an toàn.",
    "block cipher": "Block Cipher mã hóa dữ liệu theo từng block cố định (VD: DES 64-bit, AES 128-bit). Cần padding nếu plaintext không chia hết cho block size.",
    "stream cipher": "Stream Cipher mã hóa từng bit/byte một, tạo keystream từ key rồi XOR với plaintext. Ví dụ: RC4, ChaCha20. Ưu điểm: nhanh, không cần padding.",
    "padding": "Padding là thêm dữ liệu vào cuối plaintext để đủ độ dài block size. Ví dụ: PKCS#7 padding thêm byte có giá trị = số byte cần thêm (nếu thiếu 3 byte → thêm '030303').",
    "cryptanalysis": "Cryptanalysis là nghệ thuật phá mã, tìm plaintext hoặc key từ ciphertext mà không biết key. Các phương pháp: brute-force, frequency analysis, known-plaintext attack, chosen-plaintext attack.",
    "brute force": "Brute Force Attack: thử tất cả khóa có thể cho đến khi tìm ra key đúng. Hiệu quả với:\n- Caesar (26 khóa)\n- DES (2⁵⁶ khóa - có thể với máy mạnh)\nKhông khả thi với AES (2¹²⁸ khóa trở lên).",
    "frequency analysis": "Frequency Analysis: phân tích tần suất xuất hiện ký tự/bigram/trigram trong ciphertext để phá mã Substitution. Dựa trên: E, T, A, O xuất hiện nhiều nhất trong tiếng Anh.",
    "diffusion": "Diffusion (lan tỏa): tính chất mà thay đổi 1 bit plaintext ảnh hưởng đến nhiều bit ciphertext. MixColumns trong AES tạo diffusion.",
    "confusion": "Confusion (làm rối): làm mờ mối quan hệ giữa key và ciphertext. S-box trong DES/AES tạo confusion.",
}

# Keywords mapping - mở rộng với nhiều từ khóa hơn
KEYWORDS = {
    "caesar": ["caesar", "shift", "dịch chuyển", "rot", "c=p+k"],
    "substitution": [
        "substitution",
        "monoalphabetic",
        "hill",
        "quadgram",
        "thay thế",
        "ánh xạ",
        "mapping",
    ],
    "vigenere": [
        "vigenere",
        "vigenère",
        "ic",
        "index of coincidence",
        "kasiski",
        "polyalphabetic",
    ],
    "des": [
        "des",
        "feistel",
        "data encryption standard",
        "s-box",
        "56-bit",
        "64-bit block",
    ],
    "aes": [
        "aes",
        "rijndael",
        "advanced encryption",
        "subbytes",
        "mixcolumns",
        "128-bit",
        "256-bit",
    ],
    "modes": [
        "ecb",
        "cbc",
        "mode",
        "iv",
        "electronic codebook",
        "cipher block chaining",
        "initialization vector",
    ],
    "security": [
        "an toàn",
        "bảo mật",
        "security",
        "safe",
        "secure",
        "best practice",
        "nguyên tắc",
    ],
    "task1": ["task 1", "task1", "phá caesar", "break caesar"],
    "task2": ["task 2", "task2", "phá substitution", "break substitution"],
    "task3": ["task 3", "task3", "phá vigenere", "break vigenere"],
    "task4": ["task 4", "task4", "des encrypt", "des decrypt", "mã hóa des"],
    "task5": ["task 5", "task5", "aes encrypt", "aes decrypt", "mã hóa aes"],
    "general": [
        "mã hóa",
        "encryption",
        "plaintext",
        "ciphertext",
        "key",
        "khóa",
        "block cipher",
        "stream cipher",
    ],
}


def find_best_match(query: str):
    """Tìm câu trả lời phù hợp nhất từ knowledge base."""
    q = query.lower().strip()

    # Exact match trong FAQ
    for k, v in FAQ.items():
        if k.lower() == q or k in q:
            return v

    # Partial match trong FAQ keys
    for k, v in FAQ.items():
        if k in q or q in k:
            return v

    # Keyword matching với scoring
    best_topic = None
    best_score = 0
    for topic, kws in KEYWORDS.items():
        score = sum(1 for kw in kws if kw.lower() in q)
        if score > best_score:
            best_score = score
            best_topic = topic

    if best_topic and best_score > 0:
        kb = KNOWLEDGE_BASE.get(best_topic, {})
        if "description" in kb:
            # Trả về description chi tiết
            result = kb["description"]
            if "algorithm" in kb:
                result += "\n\n" + kb["algorithm"]
            elif "breaking" in kb:
                result += "\n\n" + kb["breaking"]
            return result

    return None


def get_response(user_message: str) -> str:
    """
    Trả lời tin nhắn bằng knowledge base offline.
    Trả về câu trả lời hoặc None để backend thử Gemini API.
    """
    msg = user_message.strip()
    if not msg:
        return "Vui lòng nhập nội dung câu hỏi."

    # Chào hỏi
    greetings = ["hello", "hi", "chào", "xin chào", "hey", "helo", "hii"]
    if any(g in msg.lower() for g in greetings) and len(msg.split()) <= 3:
        return """Xin chào! 👋

Tôi là **Crypto Assistant** - trợ lý mã hóa của bạn!

Tôi có thể giúp bạn với:
🔐 **Classical Ciphers:** Caesar, Substitution, Vigenère
🔒 **Modern Ciphers:** DES, AES (ECB/CBC modes)
📚 **Cryptography Concepts:** IC, Quadgram, S-box, Feistel, ...
💡 **Tasks 1-5:** Hướng dẫn sử dụng từng task

Bạn có thể hỏi:
- "Caesar là gì?"
- "Cách phá Substitution?"
- "Sự khác biệt giữa ECB và CBC?"
- "Hướng dẫn Task 2"
- "AES an toàn không?"

Hãy hỏi tôi bất cứ điều gì về mã hóa! 🚀"""

    # Câu hỏi về trợ giúp
    help_keywords = ["help", "giúp", "hỗ trợ", "hướng dẫn", "làm gì", "có thể", "biết"]
    if any(h in msg.lower() for h in help_keywords) and len(msg.split()) <= 5:
        return """📖 **Hướng dẫn sử dụng Chatbot**

Tôi có thể trả lời các câu hỏi về:

**1. Classical Ciphers (Mã hóa cổ điển):**
   - Caesar Cipher
   - Substitution Cipher
   - Vigenère Cipher

**2. Modern Ciphers (Mã hóa hiện đại):**
   - DES (Data Encryption Standard)
   - AES (Advanced Encryption Standard)

**3. Modes of Operation:**
   - ECB (Electronic Codebook)
   - CBC (Cipher Block Chaining)

**4. Cryptanalysis (Phá mã):**
   - Frequency Analysis
   - Hill Climbing
   - Index of Coincidence (IC)
   - Quadgram Scoring

**5. Tasks trong Project:**
   - Task 1: Caesar Breaker
   - Task 2: Substitution Breaker
   - Task 3: Vigenère Breaker
   - Task 4: DES Encrypt/Decrypt
   - Task 5: AES Encrypt/Decrypt

**Ví dụ câu hỏi:**
- "AES hoạt động như thế nào?"
- "Tại sao ECB không an toàn?"
- "Hướng dẫn Task 2"
- "Key của DES có bao nhiêu bit?"
- "Sự khác biệt giữa AES và DES?"

Hãy thử hỏi tôi! 😊"""

    # Tìm kiếm trong knowledge base
    answer = find_best_match(msg)
    if answer:
        return answer

    # Câu hỏi so sánh (A vs B)
    if " vs " in msg.lower() or " và " in msg.lower():
        msg_lower = msg.lower()
        comparisons = {
            ("aes", "des"): KNOWLEDGE_BASE["aes"]["comparison"],
            ("des", "aes"): KNOWLEDGE_BASE["aes"]["comparison"],
            ("ecb", "cbc"): KNOWLEDGE_BASE["modes"]["comparison"],
            ("cbc", "ecb"): KNOWLEDGE_BASE["modes"]["comparison"],
        }
        for (term1, term2), result in comparisons.items():
            if term1 in msg_lower and term2 in msg_lower:
                return result

    # Câu hỏi về ví dụ
    if "ví dụ" in msg.lower() or "example" in msg.lower():
        for cipher in ["caesar", "substitution", "vigenere", "des", "aes"]:
            if cipher in msg.lower():
                kb = KNOWLEDGE_BASE.get(cipher, {})
                if "example" in kb:
                    return f"**Ví dụ {cipher.upper()}:**\n\n{kb['example']}"

    # Câu hỏi về độ an toàn
    if any(
        w in msg.lower() for w in ["an toàn", "bảo mật", "secure", "safe", "security"]
    ):
        for cipher in ["caesar", "substitution", "vigenere", "des", "aes"]:
            if cipher in msg.lower():
                kb = KNOWLEDGE_BASE.get(cipher, {})
                if "security" in kb:
                    return f"**Độ bảo mật của {cipher.upper()}:**\n\n{kb['security']}"

    # Câu hỏi về lỗi
    error_keywords = ["lỗi", "error", "không hoạt động", "không chạy", "bị lỗi"]
    if any(e in msg.lower() for e in error_keywords):
        return """**Xử lý lỗi thường gặp:**

🔴 **Lỗi Key không hợp lệ:**
   - Kiểm tra độ dài key (DES: 16 hex, AES-128: 32 hex)
   - Key phải là hex characters (0-9, A-F)
   
🔴 **Lỗi IV không hợp lệ:**
   - CBC mode bắt buộc phải có IV
   - DES IV: 16 hex chars, AES IV: 32 hex chars
   
🔴 **Lỗi Padding:**
   - Decrypt với key sai
   - Ciphertext bị corrupt

🔴 **Upload file thất bại:**
   - Chỉ chấp nhận file .txt
   - Tối đa 15000 ký tự

Nếu vẫn gặp lỗi, hãy mô tả chi tiết hơn để tôi hỗ trợ!"""

    # Fallback: Không tìm thấy câu trả lời
    # Trả về '??' để backend biết gọi Gemini API
    return f"""🤔 Xin lỗi, tôi chưa có câu trả lời cụ thể cho câu hỏi này trong knowledge base.

**Gợi ý:**
- Thử hỏi về: Caesar, Substitution, Vigenère, DES, AES
- Hoặc về: ECB, CBC, IV, Key, Padding, Security
- Hoặc: "Hướng dẫn Task 1/2/3/4/5"

**Câu hỏi của bạn:** "{msg}"

Tôi đang chuyển tiếp cho Gemini AI để được hỗ trợ tốt hơn... ⏳"""
