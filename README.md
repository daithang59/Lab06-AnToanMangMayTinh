# 🔐 Lab06 - Review of Encryption Algorithms

[![Flask](https://img.shields.io/badge/Flask-3.0+-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Web-based Cryptography Tool** - Phân tích, giải mã và mã hóa với các thuật toán mã hóa cổ điển và hiện đại

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

#### **Task 4: DES (Data Encryption Standard)**
- Triển khai hoàn chỉnh DES từ đầu
- Hỗ trợ modes: ECB, CBC
- Input/Output: Hex format
- Key: 16 hex chars (8 bytes)
- IV auto-generation cho CBC mode

#### **Task 5: AES-128 (Advanced Encryption Standard)**
- Triển khai AES-128 từ cơ bản
- Hỗ trợ modes: ECB, CBC
- Input/Output: Hex format
- Key: 32 hex chars (16 bytes)
- IV auto-generation cho CBC mode

### 🎨 UI/UX Features

- ✅ **Dark/Light Mode** với theme toggle
- ✅ **Responsive Design** - hoạt động tốt trên mọi thiết bị
- ✅ **Copy to Clipboard** - copy kết quả một cú click
- ✅ **File Upload** hoặc Text Input trực tiếp
- ✅ **Real-time Validation** với error messages rõ ràng
- ✅ **Glass Morphism UI** với animations mượt mà
- ✅ **GitHub Integration** - link trực tiếp đến repository

## 🎬 Demo

### Local Demo
```bash
python app.py
# Truy cập: http://localhost:5000
```

## 🛠️ Công Nghệ

### Backend
- **Flask** 3.0+ - Web framework
- **Python** 3.8+ - Core language
- **Custom Crypto** - Tự triển khai tất cả algorithms

### Frontend
- **Bootstrap** 5.3 - UI framework
- **Bootstrap Icons** - Icon set
- **Vanilla JavaScript** - Interactivity
- **CSS Variables** - Dynamic theming

### Algorithms
- Chi-Square, Quadgram, IC Statistics
- Hill-Climbing, Simulated Annealing
- DES (S-boxes, P-boxes, Feistel network)
- AES (SubBytes, ShiftRows, MixColumns, KeyExpansion)

## 📦 Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.8 trở lên
- pip (Python package manager)
- 50MB dung lượng trống

### Các Bước Cài Đặt

#### 1️⃣ Clone Repository
```bash
git clone https://github.com/daithang59/Lab06-AnToanMangMayTinh.git
cd Lab06-AnToanMangMayTinh
```

#### 2️⃣ Tạo Virtual Environment (Khuyên dùng)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ Chạy Ứng Dụng
```bash
python app.py
```

#### 5️⃣ Mở Trình Duyệt
Truy cập: `http://localhost:5000`

## 🚀 Sử Dụng

### Task 1-3: Cryptanalysis
1. Chọn tab tương ứng (Caesar/Substitution/Vigenère)
2. Upload file `.txt` hoặc nhập trực tiếp ciphertext
3. Click "Decrypt" hoặc "Break Cipher"
4. Xem kết quả: Key được tìm thấy và plaintext
5. Click "Copy" để copy plaintext

### Task 4-5: Encryption/Decryption
1. Chọn tab DES hoặc AES
2. Chọn chế độ: **Encrypt** hoặc **Decrypt**
3. Chọn Mode: **ECB** hoặc **CBC**
4. Nhập Key (hex format):
   - DES: 16 hex chars (8 bytes)
   - AES: 32 hex chars (16 bytes)
5. Nhập IV nếu dùng CBC mode (encrypt có thể để trống)
6. Upload file hoặc nhập text/hex
7. Click "Thực hiện"
8. Copy kết quả nếu cần

### Tips
- **Encrypt**: Input là plaintext → Output là hex
- **Decrypt**: Input là hex → Output là plaintext
- **CBC Encrypt**: IV tự động sinh nếu không nhập
- **CBC Decrypt**: IV bắt buộc phải nhập (lấy từ khi encrypt)

## 📁 Cấu Trúc Thư Mục

```
Lab06-AnToanMangMayTinh/
│
├── 📄 app.py                    # Flask application (entry point)
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Documentation (file này)
│
├── 📁 crypto/                   # Crypto algorithms (tự triển khai)
│   ├── __init__.py
│   ├── caesar.py               # Task 1: Caesar breaker
│   ├── substitution.py         # Task 2: Substitution breaker
│   ├── vigenere.py             # Task 3: Vigenère breaker
│   ├── des_core.py             # DES 1-block implementation
│   ├── des_modes.py            # DES ECB/CBC modes
│   ├── aes_core.py             # AES-128 1-block implementation
│   └── aes_modes.py            # AES ECB/CBC modes
│
├── 📁 templates/
│   └── index.html              # Main UI (Bootstrap 5)
│
├── 📁 static/
│   ├── css/
│   │   └── style.css           # Custom CSS + Dark mode
│   └── js/
│       └── main.js             # UI interactions + Copy function
│
├── 📁 data/
│   ├── english_corpus.txt      # Corpus cho Task 2
│   ├── english_quadgrams.txt   # Quadgram statistics
│   ├── wordlist.txt            # Word dictionary
│   └── ...                     # Sample test files
│
└── 📁 report/                   # Documentation & Reports
    └── Lab06_Report.pdf        # Chi tiết thuật toán & phân tích
```

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
- **Block size**: 64 bits (8 bytes)
- **Key size**: 56 bits (8 bytes với parity)
- **Rounds**: 16 rounds Feistel network
- **Components**: PC1, PC2, IP, FP, E, P, 8 S-boxes
- **Modes**: ECB (độc lập), CBC (chaining)

### AES-128 (Advanced Encryption Standard)
- **Block size**: 128 bits (16 bytes)
- **Key size**: 128 bits (16 bytes)
- **Rounds**: 10 rounds
- **Components**: SubBytes, ShiftRows, MixColumns, AddRoundKey
- **Key Expansion**: 44 round keys (4 bytes mỗi key)
- **Modes**: ECB, CBC

## 👨‍💻 Tác Giả

**Huỳnh Lê Đại Thắng**
- MSSV: 23521422
- Trường: Đại học Công nghệ Thông tin - UIT
- GitHub: [@daithang59](https://github.com/daithang59)
- Email: 23521422@gm.uit.edu.vn

## 📝 License

Dự án này được phát hành dưới [MIT License](LICENSE).

## 📚 Tài Liệu Tham Khảo

1. [NIST DES Specification](https://csrc.nist.gov/publications/detail/fips/46/3/archive/1999-10-25)
2. [NIST AES Specification](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
3. [Practical Cryptography](http://practicalcryptography.com/)
4. [The Code Book by Simon Singh](https://simonsingh.net/books/the-code-book/)

---

⭐ Nếu project này hữu ích, đừng quên cho một star trên GitHub!

🐛 Phát hiện bug? [Mở issue](https://github.com/daithang59/Lab06-AnToanMangMayTinh/issues) để báo cáo.
