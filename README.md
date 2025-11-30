# Lab06-AnToanMangMayTinh

# Cau truc thu muc

Lab06-AnToanMang/
├─ app.py                  # Flask app (entry point)
├─ requirements.txt        # chứa flask, gunicorn... (không liên quan hạn chế crypto)
├─ crypto/                 # TẤT CẢ thuật toán tự code, không lib ngoài
│   ├─ __init__.py
│   ├─ caesar.py           # Task 1
│   ├─ substitution.py     # Task 2
│   ├─ vigenere.py         # Task 3
│   ├─ des_core.py         # DES 1-block
│   ├─ des_modes.py        # DES modes (ECB, CBC, hoặc khác)
│   ├─ aes_core.py         # AES 1-block
│   └─ aes_modes.py        # AES modes (ECB, CBC, hoặc khác)
├─ templates/
│   └─ index.html          # Giao diện chính (Bootstrap)
├─ static/
│   ├─ css/
│   │   └─ style.css       # Custom CSS thêm (nếu cần)
│   └─ js/
│       └─ main.js         # JS để xử lý UI (nếu cần AJAX)
├─ data/
│   ├─ english_corpus.txt  # dùng cho Task 2 (n-gram)
│   └─ wordlist.txt        # từ điển (Task 2,3 nếu muốn)
└─ report/
    └─ Lab06_Report.docx/.pdf
