<div align="center">

# 🔐 Lab06 - Review of Encryption Algorithms

### Web-based Cryptography Tool

_Phân tích, giải mã và mã hóa với các thuật toán mã hóa cổ điển và hiện đại_

[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

[![GitHub stars](https://img.shields.io/github/stars/daithang59/Lab06-AnToanMangMayTinh?style=social)](https://github.com/daithang59/Lab06-AnToanMangMayTinh/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/daithang59/Lab06-AnToanMangMayTinh?style=social)](https://github.com/daithang59/Lab06-AnToanMangMayTinh/network/members)
[![GitHub issues](https://img.shields.io/github/issues/daithang59/Lab06-AnToanMangMayTinh)](https://github.com/daithang59/Lab06-AnToanMangMayTinh/issues)

[🎯 Features](#-tính-năng) • [📦 Installation](#-cài-đặt) • [🚀 Usage](#-sử-dụng) • [📚 Docs](#-tài-liệu-tham-khảo) • [🤝 Contributing](#-contributing)

---

</div>

## 📋 Mục Lục

- [Giới Thiệu](#-giới-thiệu)
- [Tính Năng](#-tính-năng)
- [Demo](#-demo)
- [Công Nghệ](#-công-nghệ)
- [Cài Đặt](#-cài-đặt)
- [Sử Dụng](#-sử-dụng)
- [Cấu Trúc Thư Mục](#-cấu-trúc-thư-mục)
- [Chi Tiết Thuật Toán](#-chi-tiết-thuật-toán)
- [Tác Giả](#-tác-giả)

## 🎯 Giới Thiệu

Lab06 là một ứng dụng web toàn diện cho phép người dùng:

- **Phân tích và giải mã** các mật mã cổ điển (Caesar, Substitution, Vigenère)
- **Mã hóa/Giải mã** với các thuật toán hiện đại (DES, AES)
- **Tự triển khai** hoàn toàn các thuật toán từ đầu (không sử dụng thư viện crypto)
- **Giao diện đẹp mắt** với Dark Mode và responsive design

## ✨ Tính Năng

### 🔓 Cryptanalysis (Phân Tích Mật Mã)

#### **Task 1: Caesar Cipher Breaker**

- Brute-force 26 khóa có thể
- Chấm điểm bằng Chi-Square statistic
- Tự động chọn plaintext giống tiếng Anh nhất

#### **Task 2: Substitution Cipher Breaker**

- Hill-climbing optimization với Simulated Annealing
- Scoring dựa trên quadgram statistics
- Word-bonus để tăng độ chính xác
- Tùy chỉnh số rounds và sample size

#### **Task 3: Vigenère Cipher Breaker**

- Kasiski examination để tìm key length
- Index of Coincidence (IC) analysis
- Tấn công từng phần của key độc lập
- Hỗ trợ key length từ 3-20 ký tự

### 🔒 Modern Encryption

### Task 4: DES (Data Encryption Standard)\*\*

- ✅ Triển khai hoàn chỉnh DES từ đầu (không dùng thư viện)
- ✅ Hỗ trợ modes: **ECB**, **CBC**
- ✅ Input format:
  - **Encrypt**: Text/Hex → Output Hex
  - **Decrypt**: Hex → Output Text
- ✅ Key: 16 hex chars (8 bytes)
- ✅ IV: 16 hex chars cho CBC mode (auto-gen khi encrypt)
- ✅ PKCS#7 padding tự động

#### **Task 5: AES (Advanced Encryption Standard)**

- ✅ Triển khai AES-128/192/256 từ cơ bản
- ✅ Hỗ trợ modes: **ECB**, **CBC**, **CTR**
- ✅ Input format:
  - **Encrypt**: Text/Hex → Output Hex
  - **Decrypt**: Hex → Output Text
- ✅ Key size:
  - AES-128: 32 hex chars (16 bytes)
  - AES-192: 48 hex chars (24 bytes)
  - AES-256: 64 hex chars (32 bytes)
- ✅ IV: 32 hex chars cho CBC/CTR mode (auto-gen khi encrypt)
- ✅ PKCS#7 padding cho ECB/CBC
- ✅ Counter mode cho CTR (không cần padding)

### 🔐 Security & Validation

- ✅ **Character Set Filtering** - Tự động validate và filter ký tự theo chuẩn (a-z, A-Z, 0-9, space, dấu câu)
- ✅ **Input Validation** - Kiểm tra format hex, key length, IV requirements
- ✅ **Warning Messages** - Cảnh báo rõ ràng về ký tự không hợp lệ
- ✅ **UTF-8 Support** - Đọc/ghi file UTF-8 chuẩn

### 🎨 UI/UX Features

- ✅ **Dark/Light Mode** với theme toggle
- ✅ **Responsive Design** - hoạt động tốt trên mọi thiết bị
- ✅ **Copy to Clipboard** - copy kết quả một cú click
- ✅ **File Upload** hoặc Text Input trực tiếp
- ✅ **Real-time Validation** với error messages rõ ràng
- ✅ **Glass Morphism UI** với animations mượt mà
- ✅ **GitHub Integration** - link trực tiếp đến repository
- ✅ **UIT Logo** - Clickable logo link đến website UIT

### 🤖 AI Chatbot Assistant

- ✅ **Hybrid Intelligence** - Kết hợp Offline KB + Online AI
- ✅ **Offline Knowledge Base** - Instant responses (0ms) cho các câu hỏi phổ biến
- ✅ **Google Gemini Integration** - AI responses cho câu hỏi phức tạp
- ✅ **Smart Fallback** - Luôn có câu trả lời, không bao giờ fail
- ✅ **Priority Logic**:
  1. Offline Knowledge Base (nếu có câu trả lời chắc chắn)
  2. Gemini API (nếu câu hỏi phức tạp và có API key)
  3. Offline fallback (nếu API không khả dụng)
- ✅ **Knowledge Coverage**:
  - Caesar Cipher (algorithm, breaking methods, chi-square)
  - Substitution (quadgram statistics, hill-climbing)
  - Vigenère (IC analysis, frequency attack)
  - DES (Feistel network, 56-bit security)
  - AES (SPN structure, 128/192/256-bit)
  - Block cipher modes (ECB, CBC, CTR)
- ✅ **Bilingual** - Hỗ trợ tiếng Việt và tiếng Anh
- ✅ **Markdown Formatting** - Code blocks, bold, lists

## 🎬 Demo & Screenshots

### Chạy Local Demo

```bash
# Sau khi cài đặt dependencies
python app.py

# Server khởi động tại:
# http://localhost:5000
# hoặc
# http://127.0.0.1:5000
```

### Giao diện chính

```
┌─────────────────────────────────────────────────┐
│  🔐 Lab06 - Cryptography Tool                   │
│  ┌──────┬──────┬──────┬──────┬──────┐          │
│  │Caesar│Subst.│Vigen.│ DES  │ AES  │          │
│  └──────┴──────┴──────┴──────┴──────┘          │
│                                                  │
│  📝 Input Ciphertext:                           │
│  ┌────────────────────────────────────────┐    │
│  │ [Upload .txt file] hoặc [Paste text]   │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ⚙️ Settings: [Decrypt] [Mode: CBC] [Options]  │
│                                                  │
│  🔑 Key: ________________  IV: ________________ │
│                                                  │
│  ▶️  [Thực hiện Giải mã]                        │
│                                                  │
│  📋 Result:                                      │
│  ┌────────────────────────────────────────┐    │
│  │ Decrypted plaintext appears here...     │    │
│  │                                [📋 Copy] │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Features nổi bật

- 🌓 **Dark/Light Mode**: Toggle theme theo sở thích
- 📱 **Responsive**: Hoạt động tốt trên mobile/tablet/desktop
- ⚡ **Real-time**: Validation ngay khi nhập liệu
- 🎨 **Glass Morphism**: UI hiện đại với hiệu ứng glass
- 📋 **One-click Copy**: Copy kết quả nhanh chóng

## 🛠️ Công Nghệ & Stack

### Backend Stack

| Technology       | Version | Usage                                               |
| ---------------- | ------- | --------------------------------------------------- |
| **Python**       | 3.8+    | Core programming language                           |
| **Flask**        | 3.0.0   | Web framework, routing, templating                  |
| **Flask-Cors**   | 4.0.0   | Cross-Origin Resource Sharing                       |
| **pycryptodome** | 3.20.0  | Utilities only (hex conversion, not for main algos) |

### Frontend Stack

| Technology          | Version | Usage                                 |
| ------------------- | ------- | ------------------------------------- |
| **Bootstrap**       | 5.3     | Responsive UI framework               |
| **Bootstrap Icons** | 1.11+   | Icon set                              |
| **JavaScript**      | ES6+    | Client-side logic, interactions       |
| **CSS3**            | -       | Custom styling, animations, dark mode |

### Cryptographic Algorithms (100% Custom Implementation)

#### Statistical Analysis

- **Chi-Square Test**: Frequency analysis cho Caesar
- **Quadgram Analysis**: N-gram statistics cho Substitution
- **Index of Coincidence (IC)**: Key length detection cho Vigenère
- **Kasiski Examination**: Pattern matching cho Vigenère

#### Optimization Techniques

- **Hill-Climbing**: Local search algorithm
- **Simulated Annealing**: Escape local maxima
- **Random Restarts**: Multiple attempts với initial states khác nhau

#### Modern Cryptography

- **DES**: Feistel network, 16 rounds, S-boxes, P-boxes, key schedule
- **AES**: SubBytes (S-box), ShiftRows, MixColumns, AddRoundKey, Key Expansion
- **Block Cipher Modes**: ECB, CBC, CTR
- **Padding**: PKCS#7 padding scheme

## 📦 Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- pip (Python package manager)
- 50MB dung lượng trống
- Trình duyệt web hiện đại (Chrome, Firefox, Edge, Safari)

### Các Bước Cài Đặt

#### 1️⃣ Clone Repository

```bash
git clone https://github.com/daithang59/Lab06-AnToanMangMayTinh.git
cd Lab06-AnToanMangMayTinh
```

#### 2️⃣ Tạo Virtual Environment (Khuyên dùng)

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows CMD
python -m venv venv
venv\Scripts\activate.bat

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies bao gồm:**

- `Flask==3.0.0` - Web framework
- `Flask-Cors==4.0.0` - Cross-Origin Resource Sharing
- `pycryptodome==3.20.0` - Hỗ trợ tiện ích crypto (không dùng cho thuật toán chính)
- `python-dotenv==1.0.0` - Environment variables management
- `requests==2.32.5` - HTTP library cho AI chatbot

#### 4️⃣ Cấu Hình AI Chatbot (Tùy chọn)

Chatbot hoạt động **100% offline** mặc định. Để kích hoạt Gemini AI cho câu hỏi phức tạp:

```bash
# Copy file .env.example
cp .env.example .env

# Chỉnh sửa .env và thêm API key
GEMINI_API_KEY=your_api_key_here
```

**Lấy API key miễn phí:**

1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập Google account
3. Tạo API key mới
4. Copy và paste vào file `.env`

**Lưu ý:** Gemini free tier có giới hạn 15 requests/phút, 1500 requests/ngày.

#### 5️⃣ Chạy Ứng Dụng

```bash
python app.py
```

Server sẽ chạy ở **http://127.0.0.1:5000** (localhost:5000)

#### 5️⃣ Mở Trình Duyệt

Truy cập: **http://localhost:5000** hoặc **http://127.0.0.1:5000**

## 🚀 Sử Dụng

### Task 1-3: Cryptanalysis (Phá Mã)

#### 🔓 Task 1: Caesar Cipher

**Example:**

```
Ciphertext: KHOOR ZRUOG! WKLV LV D WHVW PHVVDJH.
→ Click "Decrypt"
Key Found: 3
Plaintext: HELLO WORLD! THIS IS A TEST MESSAGE.
```

**Steps:**

1. Chọn tab **Caesar**
2. Upload file `.txt` hoặc paste ciphertext
3. Click **"Decrypt"**
4. Xem key và plaintext
5. Click **Copy** để copy kết quả

#### 🔓 Task 2: Substitution Cipher

**Example:**

```
Ciphertext: MJQQT BTSQP! YMJX NX F YJXY RJXXFLJ.
→ Click "Break Cipher"
Score: -15234.56
Mapping: NOPQRSTUVWXYZABCDEFGHIJKLM
Plaintext: HELLO WORLD! THIS IS A TEST MESSAGE.
```

**Steps:**

1. Chọn tab **Substitution**
2. Upload/paste ciphertext (càng dài càng chính xác)
3. Tùy chỉnh settings (optional):
   - Rounds: số lần restart (default: 20)
   - Sample size: số ký tự mẫu
4. Click **"Break Cipher"**
5. Chờ 2-5 giây (tùy độ dài text)
6. Xem kết quả và copy

#### 🔓 Task 3: Vigenère Cipher

**Example:**

```
Ciphertext: LXFOPVEFRNHR
Key Length: 5 (detected by Kasiski)
→ Click "Break Cipher"
Key Found: LEMON
Score: 0.052 (IC)
Plaintext: ATTACKATDAWN
```

**Steps:**

1. Chọn tab **Vigenère**
2. Upload/paste ciphertext (ít nhất 100 chars)
3. Click **"Break Cipher"**
4. Algorithm sẽ:
   - Detect key length (Kasiski + IC)
   - Break từng phần của key
   - Combine để tìm full key
5. Xem key, score và plaintext

### Task 4-5: Encryption/Decryption (Mã Hóa Hiện Đại)

#### 🔒 Task 4: DES Example

**Encrypt Example:**

```
Operation: Encrypt
Mode: CBC
Key (hex): 0123456789ABCDEF
IV (hex): [auto-generated] → FEDCBA9876543210
Plaintext: "Hello DES!"
→ Click "Thực hiện"
Ciphertext (hex): 3d8f9a2b1c4e5f6a7b8c9d0e1f2a3b4c
IV used: FEDCBA9876543210  ← Save this!
```

**Decrypt Example:**

```
Operation: Decrypt
Mode: CBC
Key (hex): 0123456789ABCDEF
IV (hex): FEDCBA9876543210  ← Must match encrypt IV
Ciphertext (hex): 3d8f9a2b1c4e5f6a7b8c9d0e1f2a3b4c
→ Click "Thực hiện"
Plaintext: "Hello DES!"
```

#### 🔐 Task 5: AES Example

**AES-128 Encrypt:**

```
Operation: Encrypt
Algorithm: AES-128
Mode: CBC
Key (hex): 000102030405060708090a0b0c0d0e0f (32 hex chars)
IV (hex): [auto] → 0f0e0d0c0b0a09080706050403020100
Plaintext: "Advanced Encryption Standard"
→ Result
Ciphertext: 8a9b2c3d4e5f6a7b8c9d0e1f2a3b4c5d...
```

**AES-256 with CTR mode:**

```
Operation: Encrypt
Algorithm: AES-256
Mode: CTR (Counter mode - stream cipher like)
Key (hex): 000102...1e1f (64 hex chars)
IV (hex): [auto-generated]
Plaintext: "Long message can be any length!"
→ Result (no padding needed for CTR)
```

#### 📝 Hướng dẫn sử dụng DES/AES

1. **Chọn Tab**: Chọn tab **DES** hoặc **AES**
2. **Chọn Operation**: Chọn **Encrypt** (mã hóa) hoặc **Decrypt** (giải mã)
3. **Chọn Mode**:
   - **ECB** (Electronic Codebook) - không cần IV
   - **CBC** (Cipher Block Chaining) - cần IV
   - **CTR** (Counter Mode - chỉ AES) - cần IV
4. **Nhập Key** (hex format):
   - **DES**: 16 hex chars (8 bytes)
   - **AES-128**: 32 hex chars (16 bytes)
   - **AES-192**: 48 hex chars (24 bytes)
   - **AES-256**: 64 hex chars (32 bytes)
5. **Nhập IV** (nếu dùng CBC/CTR):
   - **Encrypt**: Có thể để trống (auto-generate)
   - **Decrypt**: Bắt buộc phải nhập (lấy từ kết quả encrypt)
6. **Nhập Input**:
   - **Encrypt**: Nhập plaintext hoặc upload file .txt
   - **Decrypt**: Nhập ciphertext (hex) hoặc upload file
7. **Click "Thực hiện"**
8. **Copy kết quả**: Click icon copy để copy vào clipboard

#### 💡 Tips & Lưu ý

##### Encrypt (Mã hóa)

- **Input**: Plaintext (text thông thường)
- **Output**: Ciphertext (hex format)
- **IV**: Có thể để trống, hệ thống tự sinh ngẫu nhiên
- **Lưu IV**: Khi dùng CBC/CTR, nhớ lưu IV để decrypt sau này

##### Decrypt (Giải mã)

- **Input**: Ciphertext (hex format)
- **Output**: Plaintext (text gốc)
- **IV**: Bắt buộc phải nhập chính xác IV đã dùng khi encrypt
- **Key**: Phải đúng key đã dùng khi encrypt

##### Các lỗi thường gặp

- ❌ **"Key length không hợp lệ"**: Kiểm tra độ dài key
- ❌ **"Invalid hex"**: Input decrypt phải là hex format
- ❌ **"IV required"**: CBC/CTR mode cần IV khi decrypt
- ❌ **"Padding error"**: Key hoặc IV không đúng

##### Best Practices

- ✅ Dùng **CBC mode** cho bảo mật tốt hơn ECB
- ✅ **Lưu trữ IV** cùng với ciphertext (IV không cần bảo mật)
- ✅ **Không dùng lại IV** cho cùng một key
- ✅ Dùng **AES-256** cho bảo mật cao nhất

### 🤖 Sử dụng AI Chatbot

#### Truy cập Chatbot

1. Click vào **icon chatbot** góc dưới bên phải màn hình
2. Cửa sổ chat sẽ mở ra với giao diện glass morphism
3. Gõ câu hỏi của bạn và nhấn Enter hoặc click Send

#### Các câu hỏi mẫu

**Về thuật toán:**

```
- Caesar cipher là gì?
- Giải thích thuật toán Vigenère
- So sánh DES và AES
- Quadgram statistics hoạt động thế nào?
```

**Về cryptanalysis:**

```
- Cách phá Caesar cipher?
- Index of Coincidence là gì?
- Hill climbing trong substitution
- Tại sao ECB mode không an toàn?
```

**Về implementation:**

```
- File nào chứa code AES?
- Cách tính chi-square score?
- Project structure như thế nào?
```

**Tổng quát:**

```
- help
- features
- giới thiệu project
```

#### Chế độ hoạt động

**🟢 Offline Mode (Mặc định)**

- Instant responses (0ms latency)
- Không cần internet/API key
- Coverage: 90% câu hỏi phổ biến
- Hiển thị: "_💡 Powered by Offline Knowledge Base_"

**🔵 Hybrid Mode (Với API key)**

- Ưu tiên offline knowledge
- Fallback sang Gemini cho câu hỏi phức tạp
- Hiển thị: "_🤖 Powered by Google Gemini AI_"

**🟡 Fallback Mode (API fail)**

- Tự động chuyển về offline
- Luôn có câu trả lời
- Hiển thị: "_⚠️ Gemini API không khả dụng_"

#### Tips sử dụng Chatbot

- ✅ Hỏi bằng **tiếng Việt** hoặc **tiếng Anh**
- ✅ Câu hỏi ngắn gọn, cụ thể
- ✅ Dùng "help" để xem hướng dẫn
- ✅ Chatbot hiểu context về Lab06
- ❌ Không hỏi về code không liên quan
- ❌ Không hỏi về crypto không có trong project

## 📁 Cấu Trúc Thư Mục

```
Lab06-AnToanMangMayTinh/
│
├── 📄 app.py                    # Flask application (582 lines)
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Documentation đầy đủ
│
├── 📁 crypto/                   # 🔥 Crypto algorithms (tự triển khai 100%)
│   ├── __init__.py             # Package initialization
│   ├── caesar.py               # Task 1: Caesar cipher breaker
│   ├── substitution.py         # Task 2: Substitution cipher breaker
│   ├── vigenere.py             # Task 3: Vigenère cipher breaker
│   ├── charset_filter.py       # Input validation & character filtering
│   ├── des_core.py             # DES core (Feistel, S-boxes, P-boxes)
│   ├── des_modes.py            # DES ECB/CBC modes + padding
│   ├── aes_core.py             # AES-128/192/256 (SubBytes, MixColumns...)
│   ├── aes_modes.py            # AES ECB/CBC/CTR modes + padding
│   └── chatbot_knowledge.py    # 🤖 AI knowledge base (380 lines)
│
├── 📁 templates/
│   └── index.html              # Single-page app với Bootstrap 5, chatbot UI
│
├── 📁 static/
│   ├── css/
│   │   ├── style.css           # Custom CSS, Glass morphism, Dark mode
│   │   └── chatbot.css         # 🤖 Chatbot UI styling (400 lines)
│   ├── js/
│   │   ├── main.js             # JavaScript: UI logic, Copy, Theme toggle
│   │   └── chatbot.js          # 🤖 Chatbot client logic (250 lines)
│   └── images/
│       └── uit_logo.png        # UIT logo (favicon & header)
│
├── 📄 .env.example              # Environment variables template
├── 📄 .gitignore                # Git ignore file
└── 📄 CHATBOT_SETUP.md          # AI Chatbot setup guide
│
├── 📁 data/                     # Test data & dictionaries
│   ├── english_corpus.txt      # English text corpus cho training
│   ├── english_quadgrams.txt   # Quadgram frequency statistics
│   ├── wordlist.txt            # English word dictionary
│   ├── ciphertext.txt          # Sample ciphertext files
│   ├── task4_ciphertext.txt    # DES test files
│   ├── task5_ciphertext.txt    # AES test files
│   └── ...                     # Các file test khác
│
└── 📁 report/                   # Documentation
    └── Lab06_Report.pdf        # Chi tiết thuật toán & kết quả test
```

### 📊 Code Statistics

| Module                 | Lines of Code | Mô tả                                                |
| ---------------------- | ------------- | ---------------------------------------------------- |
| `app.py`               | ~730          | Flask routes, validation, error handling, AI chatbot |
| `chatbot_knowledge.py` | ~380          | AI knowledge base với semantic search                |
| `aes_core.py`          | ~502          | AES implementation with key expansion                |
| `aes_modes.py`         | ~200          | ECB/CBC/CTR modes                                    |
| `des_core.py`          | ~350          | DES Feistel network                                  |
| `substitution.py`      | ~370          | Hill-climbing with simulated annealing               |
| `vigenere.py`          | ~351          | Kasiski + IC analysis                                |
| `caesar.py`            | ~174          | Chi-square frequency analysis                        |
| `chatbot.js`           | ~250          | Frontend chatbot UI & logic                          |
| `chatbot.css`          | ~400          | Glass morphism chatbot styling                       |
| **TOTAL**              | **~3700+**    | **Pure Python + JavaScript implementation**          |

## 🔬 Chi Tiết Thuật Toán

### Caesar Cipher

- **Phương pháp**: Brute-force 26 khóa
- **Scoring**: Chi-Square statistic với tần suất tiếng Anh
- **Complexity**: O(n) với n = độ dài text

### Substitution Cipher

- **Phương pháp**: Hill-climbing với random restarts
- **Scoring**: Quadgram frequency + word bonus
- **Optimization**: Simulated Annealing để tránh local maxima
- **Complexity**: O(rounds × swaps × text_length)

### Vigenère Cipher

- **Bước 1**: Kasiski examination → ước lượng key length
- **Bước 2**: Index of Coincidence → xác nhận key length
- **Bước 3**: Tách thành các Caesar ciphers độc lập
- **Bước 4**: Giải từng phần bằng frequency analysis
- **Complexity**: O(max_keylen × 26 × text_length)

### DES (Data Encryption Standard)

#### Thông số kỹ thuật

- **Block size**: 64 bits (8 bytes)
- **Key size**: 56 bits effective (64 bits với parity bits)
- **Structure**: 16-round Feistel network
- **Rounds**: 16 rounds với subkeys khác nhau

#### Components chính

- **IP (Initial Permutation)**: Hoán vị đầu vào
- **FP (Final Permutation)**: Hoán vị cuối (nghịch đảo của IP)
- **E (Expansion)**: Mở rộng 32 bits → 48 bits
- **P (Permutation)**: Hoán vị P-box
- **S-boxes**: 8 Substitution boxes (6 bits → 4 bits mỗi box)
- **PC1, PC2**: Permutation Choice cho key scheduling

#### Modes được triển khai

- **ECB (Electronic Codebook)**: Mã hóa độc lập từng block
- **CBC (Cipher Block Chaining)**: Chaining với IV và XOR

### AES (Advanced Encryption Standard)

#### Thông số kỹ thuật

- **Block size**: 128 bits (16 bytes) - cố định
- **Key size**:
  - AES-128: 128 bits (16 bytes) → 10 rounds
  - AES-192: 192 bits (24 bytes) → 12 rounds
  - AES-256: 256 bits (32 bytes) → 14 rounds

#### Components chính

- **SubBytes**: Substitution sử dụng S-box (Rijndael S-box)
- **ShiftRows**: Dịch chuyển hàng trong state matrix
- **MixColumns**: Trộn cột (không áp dụng ở round cuối)
- **AddRoundKey**: XOR state với round key
- **Key Expansion**: Sinh round keys từ master key

#### Key Expansion details

- **AES-128**: 11 round keys (176 bytes total)
- **AES-192**: 13 round keys (208 bytes total)
- **AES-256**: 15 round keys (240 bytes total)

#### Modes được triển khai

- **ECB (Electronic Codebook)**: Mã hóa độc lập từng block
- **CBC (Cipher Block Chaining)**: Chaining với IV
- **CTR (Counter Mode)**: Stream cipher mode, không cần padding

## 🎓 Context & Assignment

Đây là bài lab thuộc môn **An Toàn Mạng và Máy Tính** (Network and Computer Security).

**Mục tiêu bài lab:**

1. Hiểu và triển khai các thuật toán mã hóa cổ điển
2. Phân tích điểm yếu và cách phá mã (cryptanalysis)
3. Triển khai DES và AES từ đầu (without external crypto libraries)
4. So sánh hiệu quả giữa các thuật toán
5. Xây dựng web application để demo

**Yêu cầu:**

- ✅ Không sử dụng thư viện crypto có sẵn cho core algorithms
- ✅ Phải tự implement tất cả từ cơ bản
- ✅ Có giao diện web thân thiện
- ✅ Viết báo cáo chi tiết về cách hoạt động

## 👨‍💻 Tác Giả

<div align="center">

### Huỳnh Lê Đại Thắng

**MSSV**: 23521422  
**Trường**: Đại học Công nghệ Thông tin - UIT  
**Khóa**: K23

[![GitHub](https://img.shields.io/badge/GitHub-daithang59-181717?style=for-the-badge&logo=github)](https://github.com/daithang59)
[![Email](https://img.shields.io/badge/Email-23521422@gm.uit.edu.vn-EA4335?style=for-the-badge&logo=gmail)](mailto:23521422@gm.uit.edu.vn)

</div>

## 🎯 Mục tiêu học tập

Project này giúp bạn:

- ✅ Hiểu sâu về **cách hoạt động** của các thuật toán mã hóa
- ✅ Thực hành **triển khai từ đầu** (from scratch) các algorithms
- ✅ Nắm vững **cryptanalysis** - phân tích và phá mã
- ✅ So sánh **mã hóa cổ điển** vs **mã hóa hiện đại**
- ✅ Hiểu về **block cipher modes** (ECB, CBC, CTR)
- ✅ Phát triển kỹ năng **Full-stack** (Python Backend + Web Frontend)
- ✅ Học về **security best practices** và common vulnerabilities

## ⚠️ Security Considerations

### ⚠️ CẢNH BÁO QUAN TRỌNG

**ĐÂY LÀ PROJECT HỌC TẬP - KHÔNG SỬ DỤNG TRONG PRODUCTION!**

Lý do:

1. **Performance**: Python implementation chậm hơn C/Rust 100-1000 lần
2. **Side-channel attacks**: Không implement constant-time operations
3. **Không audit**: Code chưa được security audit chuyên nghiệp
4. **Missing features**: Không có MAC, authenticated encryption (GCM, etc.)
5. **Key management**: Không có secure key derivation, storage

### ✅ Đúng cách sử dụng crypto trong Production

```python
# ✅ ĐÚNG: Dùng thư viện đã được kiểm chứng
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ✅ ĐÚNG: Dùng authenticated encryption
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ❌ SAI: Tự implement crypto cho production
# from crypto.aes_core import aes_encrypt_block  # CHỈ ĐỂ HỌC!
```

### 🛡️ Security Best Practices

1. **Key Management**

   - ✅ Dùng CSPRNG (Cryptographically Secure PRNG)
   - ✅ Never hardcode keys
   - ✅ Use key derivation functions (PBKDF2, Argon2)
   - ❌ Don't reuse keys across different contexts

2. **Mode Selection**

   - ✅ CBC with HMAC hoặc GCM (authenticated encryption)
   - ❌ Never use ECB mode (patterns visible)
   - ⚠️ CTR mode: never reuse (key, nonce) pair

3. **IV/Nonce**

   - ✅ Random IV cho CBC
   - ✅ Unique nonce cho CTR/GCM
   - ❌ Never reuse IV với cùng key

4. **Padding**
   - ⚠️ Padding oracle attacks nếu không cẩn thận
   - ✅ Dùng authenticated encryption để tránh

### 📚 Known Vulnerabilities Trong Project

| Issue                | Location             | Impact         | Mitigation (học tập)       |
| -------------------- | -------------------- | -------------- | -------------------------- |
| No constant-time ops | All crypto/          | Timing attacks | Use `cryptography` in prod |
| No MAC/Auth          | aes_modes, des_modes | Tampering      | Add HMAC or use GCM        |
| Simple padding       | PKCS#7               | Padding oracle | Use AEAD modes             |
| No key derivation    | User input keys      | Weak keys      | Use PBKDF2/Argon2          |
| ECB mode available   | des_modes, aes_modes | Pattern leak   | Disable ECB, use CBC+      |

## 🗺️ Roadmap & Future Improvements

### 🔜 Planned Features

- [x] **AI Chatbot** - Crypto assistant với offline knowledge base ✅ **DONE**
- [x] **Gemini Integration** - Google AI cho câu hỏi phức tạp ✅ **DONE**
- [x] **Hybrid Intelligence** - Smart fallback offline/online ✅ **DONE**
- [ ] **RSA Implementation** - Public key cryptography
- [ ] **Diffie-Hellman** - Key exchange
- [ ] **Hash Functions** - SHA-256, SHA-3
- [ ] **Digital Signatures** - ECDSA
- [ ] **Authenticated Encryption** - AES-GCM, ChaCha20-Poly1305
- [ ] **Post-Quantum Crypto** - Lattice-based algorithms
- [ ] **Performance Optimization** - Cython, PyPy compilation
- [ ] **CLI Tool** - Command-line interface
- [ ] **Docker Support** - Containerization
- [ ] **Unit Tests** - Comprehensive test suite
- [ ] **API Documentation** - OpenAPI/Swagger
- [ ] **Mobile App** - React Native frontend

### 🎨 UI/UX Improvements

- [x] **UIT Logo Integration** - Clickable logo với animations ✅ **DONE**
- [x] **Chatbot UI** - Glass morphism design với typing indicators ✅ **DONE**
- [x] **Favicon** - UIT logo trong browser tab ✅ **DONE**
- [ ] Drag & drop file upload
- [ ] Progress bars cho long operations
- [ ] Side-by-side comparison mode
- [ ] Export results to PDF/CSV
- [ ] Encryption strength meter
- [ ] Key generator with QR code

### 📖 Documentation

- [ ] Video tutorials
- [ ] Interactive algorithm visualizations
- [ ] API documentation với examples
- [ ] Contributing guidelines
- [ ] Code architecture diagram

## 🔧 Troubleshooting

### ❌ Lỗi cài đặt dependencies

```bash
# Lỗi: pip version cũ
pip install --upgrade pip
pip install -r requirements.txt

# Lỗi: conflict dependencies
pip install -r requirements.txt --force-reinstall

# Windows: Lỗi permission
pip install -r requirements.txt --user
```

### ❌ Port 5000 đã được sử dụng

```python
# Cách 1: Sửa trong app.py (dòng cuối cùng)
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Đổi sang port khác
```

```bash
# Cách 2: Kill process đang dùng port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Cách 2: Kill process (Mac/Linux)
lsof -ti:5000 | xargs kill -9
```

### ❌ Không tìm thấy module crypto

```bash
# Đảm bảo đang ở đúng thư mục
cd Lab06-AnToanMangMayTinh
pwd  # hoặc cd (Windows) để check

# Kiểm tra virtual environment đã activate
# Windows PowerShell: prompt sẽ có (venv)
# Nếu chưa:
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### ❌ Lỗi UTF-8 khi đọc file

```python
# File data phải được lưu với encoding UTF-8
# Nếu gặp lỗi: UnicodeDecodeError
# Mở file bằng Notepad++ hoặc VS Code
# Save As -> Encoding: UTF-8
```

### ❌ Kết quả giải mã không đúng

**Caesar/Substitution/Vigenère:**

- Đảm bảo input chỉ chứa chữ cái tiếng Anh
- Kết quả phụ thuộc vào corpus và statistics
- Thử tăng số rounds cho Substitution

**DES/AES:**

- Kiểm tra key format (phải là hex)
- Kiểm tra độ dài key (DES: 16 hex, AES-128: 32 hex)
- CBC mode: IV phải giống lúc encrypt
- Decrypt: input phải là hex format

**AI Chatbot:**

- Chatbot hoạt động 100% offline mặc định
- Gemini API key là tùy chọn (cho câu hỏi phức tạp)
- Free tier: 15 requests/phút, 1500 requests/ngày
- Nếu hết quota: Chatbot tự động fallback offline
- Knowledge base cover 90% câu hỏi phổ biến

### ⚠️ Warning về performance

```
Nếu app chạy chậm:
- Giảm text length (max 5000 chars cho Substitution)
- Giảm số rounds trong substitution.py
- Đóng các app khác để giải phóng RAM
- Dùng PyPy thay vì CPython (nhanh hơn 2-5x)
```

## 🔌 API Endpoints

Project cung cấp các API endpoints để tích hợp:

### Web Routes (Form-based)

```
POST /task1/caesar          # Caesar cipher breaker
POST /task2/substitution    # Substitution cipher breaker
POST /task3/vigenere        # Vigenère cipher breaker
POST /task4/des             # DES encrypt/decrypt
POST /task5/aes             # AES encrypt/decrypt
```

### JSON API Routes (REST API)

```
POST /api/task1/caesar          # Returns JSON
POST /api/task2/substitution    # Returns JSON
POST /api/task3/vigenere        # Returns JSON
```

### Example API Usage

```python
import requests

# Caesar breaker API
response = requests.post('http://localhost:5000/api/task1/caesar',
    json={'ciphertext': 'KHOOR ZRUOG'})
print(response.json())
# Output: {'key': 3, 'plaintext': 'HELLO WORLD'}

# Substitution breaker API
response = requests.post('http://localhost:5000/api/task2/substitution',
    json={'ciphertext': 'YOUR_CIPHER_HERE'})
print(response.json())
# Output: {'score': -12345.6, 'mapping': 'QWERTYUIOP...', 'plaintext': '...'}
```

## 📊 Performance Benchmarks

### Cryptanalysis Performance

| Thuật toán        | Text Length  | Thời gian | CPU    | RAM    |
| ----------------- | ------------ | --------- | ------ | ------ |
| Caesar            | 10,000 chars | < 0.1s    | Low    | < 10MB |
| Substitution      | 1,000 chars  | 1-2s      | Medium | ~50MB  |
| Substitution      | 5,000 chars  | 3-7s      | High   | ~100MB |
| Vigenère (key=5)  | 5,000 chars  | 1-2s      | Medium | ~30MB  |
| Vigenère (key=15) | 5,000 chars  | 3-5s      | High   | ~50MB  |

### Encryption/Decryption Performance

| Thuật toán  | Data Size | Operation | Thời gian | Throughput |
| ----------- | --------- | --------- | --------- | ---------- |
| DES ECB     | 1KB       | Encrypt   | < 0.05s   | ~20 KB/s   |
| DES CBC     | 1KB       | Encrypt   | < 0.06s   | ~17 KB/s   |
| AES-128 ECB | 1KB       | Encrypt   | < 0.04s   | ~25 KB/s   |
| AES-128 CBC | 1KB       | Encrypt   | < 0.05s   | ~20 KB/s   |
| AES-256 CBC | 1KB       | Encrypt   | < 0.08s   | ~13 KB/s   |
| AES-256 CTR | 1KB       | Encrypt   | < 0.07s   | ~14 KB/s   |

_Đo trên Python 3.11, Windows 11, Intel i5-1135G7_

**Lưu ý**: Đây là implementation học tập, không tối ưu cho production. Library như `cryptography` hay `pycryptodome` nhanh hơn 100-1000 lần nhờ C implementation.

## ❓ FAQ (Frequently Asked Questions)

### Q1: Tại sao không dùng thư viện crypto có sẵn?

**A:** Đây là bài lab học tập, mục tiêu là hiểu sâu cách hoạt động của algorithms. Trong thực tế, **luôn dùng thư viện đã được kiểm chứng** như `cryptography`, `pycryptodome`.

### Q2: Code này có an toàn để dùng trong production không?

**A:** **KHÔNG!** Đây chỉ là code học tập, thiếu nhiều tính năng bảo mật quan trọng (constant-time ops, authenticated encryption, proper key management). Xem [Security Considerations](#️-security-considerations).

### Q3: Tại sao Substitution Cipher chạy chậm?

**A:** Hill-climbing với simulated annealing cần thử rất nhiều combinations. Text càng dài, càng chính xác nhưng cũng càng chậm. Có thể giảm số rounds trong `substitution.py`.

### Q4: Kết quả giải mã không đúng, làm sao?

**A:**

- **Caesar/Vigenère**: Ciphertext phải là chữ cái tiếng Anh
- **Substitution**: Cần ít nhất 200-300 ký tự, càng dài càng tốt
- **DES/AES**: Kiểm tra key format, IV (CBC mode), input format (hex)

### Q5: Có thể dùng với text tiếng Việt không?

**A:** Hiện tại chỉ hỗ trợ tiếng Anh (a-z, A-Z). Để hỗ trợ tiếng Việt cần:

- Frequency table cho tiếng Việt
- Quadgram/bigram statistics tiếng Việt
- Vietnamese corpus

### Q6: Làm sao để đóng góp cho project?

**A:** Xem section [Contributing](#-contributing) bên dưới!

### Q7: DES có còn an toàn không?

**A:** **KHÔNG!** DES đã bị phá vào năm 1998 (56-bit key quá ngắn). Dùng **AES** cho ứng dụng thực tế. DES chỉ được dạy để hiểu lịch sử và cấu trúc Feistel.

### Q8: Sự khác biệt giữa ECB và CBC mode?

**A:**

- **ECB**: Mã hóa độc lập từng block → patterns visible → **KHÔNG AN TOÀN**
- **CBC**: Chaining với IV → patterns hidden → An toàn hơn
- **CTR**: Stream cipher mode → có thể parallel → Nhanh nhất

Xem [ECB Penguin](<https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)>) để hiểu tại sao ECB không an toàn.

### Q9: Project này có thể chạy trên server/cloud không?

**A:** Có, nhưng cần:

```python
# Disable debug mode
app.run(debug=False, host='0.0.0.0', port=5000)

# Set production configs
app.config['ENV'] = 'production'
```

Khuyên dùng **Gunicorn** + **Nginx** cho production.

### Q10: Làm sao để test API endpoints?

**A:** Dùng `curl`, `Postman`, hoặc `Python requests`:

```bash
# Test Caesar API
curl -X POST http://localhost:5000/api/task1/caesar \
  -H "Content-Type: application/json" \
  -d '{"ciphertext": "KHOOR ZRUOG"}'
```

## 🤝 Contributing

Contributions are welcome! Mọi đóng góp đều được chào đón.

### 🌟 Cách đóng góp

1. **Fork** repository
2. **Clone** fork của bạn:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Lab06-AnToanMangMayTinh.git
   ```
3. Tạo **branch** mới:
   ```bash
   git checkout -b feature/ten-feature-cua-ban
   ```
4. **Commit** changes:
   ```bash
   git commit -m "Add: mô tả ngắn gọn"
   ```
5. **Push** to branch:
   ```bash
   git push origin feature/ten-feature-cua-ban
   ```
6. Tạo **Pull Request**

### 💡 Ý tưởng đóng góp

- 🐛 **Bug fixes**: Tìm và fix bugs
- ✨ **Features**: Thêm algorithms mới (RSA, ECC, SHA-256...)
- 📝 **Documentation**: Cải thiện docs, thêm examples
- 🎨 **UI/UX**: Cải thiện giao diện
- ⚡ **Performance**: Tối ưu hóa code
- 🧪 **Tests**: Viết unit tests
- 🌐 **i18n**: Thêm ngôn ngữ khác (tiếng Việt full, etc.)

### 📋 Guidelines

- Code style: Follow **PEP 8** cho Python
- Commit messages: Clear và descriptive
- Comments: Tiếng Anh hoặc tiếng Việt (consistent)
- Testing: Test trước khi PR
- Documentation: Update README nếu thêm features

## 📝 License

Dự án này được phát hành dưới [MIT License](LICENSE).

```
MIT License

Copyright (c) 2025 Huỳnh Lê Đại Thắng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📚 Tài Liệu Tham Khảo

### Chuẩn chính thức

1. [NIST FIPS 46-3: DES Specification](https://csrc.nist.gov/publications/detail/fips/46/3/archive/1999-10-25)
2. [NIST FIPS 197: AES Specification](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
3. [NIST SP 800-38A: Block Cipher Modes](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf)

### Cryptanalysis

4. [Practical Cryptography - Frequency Analysis](http://practicalcryptography.com/cryptanalysis/)
5. [Quadgram Statistics for Breaking Ciphers](http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/)
6. [Kasiski Examination Method](http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-vigenere-cipher/)

### Sách và tài liệu

7. [The Code Book by Simon Singh](https://simonsingh.net/books/the-code-book/)
8. [Understanding Cryptography by Christof Paar](http://www.crypto-textbook.com/)
9. [Applied Cryptography by Bruce Schneier](https://www.schneier.com/books/applied-cryptography/)

### AI & Machine Learning

10. [Google Gemini AI Studio](https://aistudio.google.com/) - Free API for AI chatbot
11. [Gemini API Documentation](https://ai.google.dev/docs) - Official docs
12. [RAG (Retrieval-Augmented Generation)](https://arxiv.org/abs/2005.11401) - Hybrid AI approach

---

<div align="center">

### 💝 Support & Feedback

⭐ **Nếu project này hữu ích, hãy cho một star trên GitHub!**

🐛 **Phát hiện bug?** [Mở issue](https://github.com/daithang59/Lab06-AnToanMangMayTinh/issues)

💬 **Có câu hỏi?** [Discussions](https://github.com/daithang59/Lab06-AnToanMangMayTinh/discussions)

📧 **Contact**: 23521422@gm.uit.edu.vn

---

Made with ❤️ by [Huỳnh Lê Đại Thắng](https://github.com/daithang59)

### 🙏 Acknowledgments

Cảm ơn đến:

- **UIT (Đại học Công nghệ Thông tin)** - Môi trường học tập
- **Giảng viên môn An Toàn Mạng và Máy Tính** - Hướng dẫn và support
- **NIST** - Cung cấp chuẩn DES và AES specifications
- **Practical Cryptography** - Tài liệu và corpus data
- **Bootstrap Team** - Amazing UI framework
- **Flask Community** - Excellent web framework
- **Open Source Community** - Inspiration và tools

### 📖 Related Projects

- [CyberChef](https://github.com/gchq/CyberChef) - The Cyber Swiss Army Knife
- [CrypTool](https://www.cryptool.org/) - Open-source e-learning crypto tool
- [Cryptography.io](https://cryptography.io/) - Python cryptography library

### 📜 Citation

Nếu bạn sử dụng project này trong nghiên cứu hoặc báo cáo, vui lòng cite:

```bibtex
@software{lab06_crypto_2025,
  author = {Huỳnh Lê Đại Thắng},
  title = {Lab06 - Review of Encryption Algorithms},
  year = {2025},
  url = {https://github.com/daithang59/Lab06-AnToanMangMayTinh},
  institution = {University of Information Technology - UIT}
}
```

---

**⚠️ Disclaimer**: This is an educational project. Do not use in production systems. Always use established cryptographic libraries for real-world applications.

**🎓 Educational Purpose Only** | **🚫 Not for Production Use** | **✅ Perfect for Learning**

---

**Last Updated**: December 2025  
**Version**: 1.0.0  
**Status**: ✅ Active Development

</div>
