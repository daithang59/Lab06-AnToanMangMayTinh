from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import string
from dotenv import load_dotenv
import requests
import time

# Load environment variables
load_dotenv()

# Import các module crypto bạn sẽ tự cài đặt
from crypto.caesar import break_caesar
from crypto.substitution import break_substitution
from crypto.vigenere import break_vigenere
from crypto.des_modes import des_encrypt, des_decrypt
from crypto.aes_modes import aes_encrypt, aes_decrypt
from crypto.charset_filter import validate_and_filter

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ALPHABET = string.ascii_lowercase

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "change-this-secret-key"  # nếu sau này bạn dùng flash, session, v.v.
)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# File upload configuration
MAX_CONTENT_LENGTH = 10000  # 10000 characters
ALLOWED_EXTENSIONS = {"txt"}


def allowed_file(filename):
    """Check if file has allowed extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_text_length(text, max_length=MAX_CONTENT_LENGTH):
    """Validate text length"""
    if len(text) > max_length:
        return (
            False,
            f"Text quá dài. Tối đa {max_length} ký tự (hiện tại: {len(text)} ký tự).",
        )
    return True, None


def process_input(file, text_input):
    """
    Process file upload or text input with validation.
    Returns: (success, data_or_error_message)
    """
    data = None

    # Priority: text input > file
    if text_input and text_input.strip():
        data = text_input.strip()
    elif file and file.filename:
        # Validate file extension
        if not allowed_file(file.filename):
            return False, "Chỉ chấp nhận file .txt"
        # Read file
        try:
            data = file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            return False, f"Lỗi đọc file: {str(e)}"

    if not data:
        return False, "Vui lòng upload file .txt HOẶC nhập text trực tiếp"

    # Validate length
    is_valid, error_msg = validate_text_length(data)
    if not is_valid:
        return False, error_msg

    return True, data


@app.route("/")
def index():
    """
    Trang chính: mặc định active_tab = task1.
    """
    return render_template("index.html", active_tab="task1")


# ====================
# TASK 1 – CAESAR
# ====================
@app.route("/task1/caesar", methods=["POST"])
def task1_caesar():
    file = request.files.get("cipher_file")
    cipher_text = request.form.get("cipher_text") or ""

    # Process and validate input
    success, result = process_input(file, cipher_text)
    if not success:
        return render_template(
            "index.html",
            active_tab="task1",
            task1_result=f"ERROR: {result}",
            task1_key="",
        )

    ciphertext = result

    # Validate và filter charset
    is_valid, filtered_text, warning = validate_and_filter(ciphertext, "Caesar")
    if warning:
        # Có ký tự không hợp lệ, hiển thị warning nhưng vẫn tiếp tục xử lý
        ciphertext = filtered_text
        warning_msg = f"\n{warning}\n\n"
    else:
        warning_msg = ""

    # Gọi hàm giải Caesar
    key, plaintext = break_caesar(ciphertext)

    return render_template(
        "index.html",
        active_tab="task1",
        task1_key=key,
        task1_result=warning_msg + plaintext,
    )


# ====================
# TASK 2 – SUBSTITUTION
# ====================
@app.route("/task2/substitution", methods=["POST"])
def task2_substitution():
    file = request.files.get("cipher_file")
    cipher_text = request.form.get("cipher_text") or ""

    # Process and validate input
    success, result = process_input(file, cipher_text)
    if not success:
        return render_template(
            "index.html",
            active_tab="task2",
            task2_result=f"ERROR: {result}",
            task2_score="",
            task2_mapping="",
        )

    ciphertext = result

    # Validate và filter charset
    is_valid, filtered_text, warning = validate_and_filter(ciphertext, "Substitution")
    if warning:
        ciphertext = filtered_text
        warning_msg = f"\n{warning}\n\n"
    else:
        warning_msg = ""

    # Gọi hàm crack substitution
    score, mapping_str, plaintext = break_substitution(ciphertext)

    # Parse mapping_str để extract plain alphabet ONLY
    # Format: "CIPHER: ABC... | PLAIN : XYZ..."
    plain_alphabet = ALPHABET.upper()  # default
    cipher_alphabet = ALPHABET.upper()

    # Debug logging
    print(f"DEBUG - mapping_str: {mapping_str}")
    print(f"DEBUG - Contains pipe: {'|' in mapping_str}")

    if "|" in mapping_str:
        # Split by pipe
        parts = mapping_str.split("|")
        print(f"DEBUG - Parts: {parts}")
        for part in parts:
            part_lower = part.lower().strip()
            print(f"DEBUG - Part lower: {part_lower}")
            if part_lower.startswith("plain"):
                # Extract chỉ phần alphabet sau dấu ":"
                plain_alphabet = part.split(":")[-1].strip().upper()
                print(f"DEBUG - Plain alphabet: {plain_alphabet}")
            elif part_lower.startswith("cipher"):
                cipher_alphabet = part.split(":")[-1].strip().upper()
                print(f"DEBUG - Cipher alphabet: {cipher_alphabet}")

    # Format score rõ ràng hơn
    score_display = f"{score:.2f}"

    return render_template(
        "index.html",
        active_tab="task2",
        task2_score=score_display,
        task2_cipher=cipher_alphabet,  # Cipher alphabet
        task2_mapping=plain_alphabet,  # Plain alphabet only
        task2_result=warning_msg + plaintext,
    )


# ====================
# TASK 3 – VIGENERE
# ====================
@app.route("/task3/vigenere", methods=["POST"])
def task3_vigenere():
    file = request.files.get("cipher_file")
    cipher_text = request.form.get("cipher_text") or ""

    # Process and validate input
    success, result = process_input(file, cipher_text)
    if not success:
        return render_template(
            "index.html",
            active_tab="task3",
            task3_result=f"ERROR: {result}",
            task3_key="",
            task3_score="",
        )

    ciphertext = result

    # Validate và filter charset
    is_valid, filtered_text, warning = validate_and_filter(ciphertext, "Vigenère")
    if warning:
        ciphertext = filtered_text
        warning_msg = f"\n{warning}\n\n"
    else:
        warning_msg = ""

    # ➜ nhận 3 giá trị
    key, plaintext, score = break_vigenere(ciphertext)

    return render_template(
        "index.html",
        active_tab="task3",
        task3_key=key,
        task3_result=warning_msg + plaintext,
        task3_score=score,
    )


# ====================
# TASK 4 – DES
# ====================
@app.route("/task4/des", methods=["POST"])
def task4_des():
    file = request.files.get("input_file")
    plaintext_input = request.form.get("plaintext_input") or ""
    mode = request.form.get("mode")  # 'ECB' hoặc 'CBC' ...
    action = request.form.get("action")  # 'encrypt' hoặc 'decrypt'
    key_hex = request.form.get("key") or ""
    iv_hex = request.form.get("iv") or ""

    if not mode or not action or not key_hex:
        return redirect(url_for("index"))

    # Xử lý input
    data = None
    if plaintext_input.strip():
        # Người dùng nhập vào textarea
        # Nếu là decrypt → coi như hex, nếu encrypt → coi như plaintext
        if action == "decrypt":
            # Decrypt: input phải là hex
            hex_text = "".join(plaintext_input.split())
            try:
                data = bytes.fromhex(hex_text)
            except ValueError:
                return render_template(
                    "index.html",
                    active_tab="task4",
                    task4_result="ERROR: Khi decrypt, input phải là hex. Paste ciphertext hex vào ô textarea.",
                    task4_iv="",
                )
        else:
            # Encrypt: input là plaintext
            data = plaintext_input.encode("utf-8")
    elif file and file.filename:
        # Đọc file content
        file_content = file.read().decode("utf-8", errors="ignore")

        if action == "decrypt":
            # Decrypt: file phải chứa hex
            hex_text = "".join(file_content.split())
            try:
                data = bytes.fromhex(hex_text)
            except ValueError:
                return render_template(
                    "index.html",
                    active_tab="task4",
                    task4_result="ERROR: Khi decrypt, file phải chứa chuỗi hex hợp lệ.",
                    task4_iv="",
                )
        else:
            # Encrypt: file chứa plaintext
            data = file_content.encode("utf-8")

    if data is None:
        return render_template(
            "index.html",
            active_tab="task4",
            task4_result="ERROR: Phải upload file hex HOẶC nhập vào textarea.",
            task4_iv="",
        )

    # Key - chấp nhận hex hoặc plaintext
    key_format = request.form.get("key_format") or "hex"
    key_input = request.form.get("key") or ""
    key_input = key_input.strip()

    if key_format == "plaintext":
        # Nếu là plaintext, chuyển thành bytes rồi kiểm tra độ dài
        key = key_input.encode("utf-8")
        if len(key) != 8:
            return render_template(
                "index.html",
                active_tab="task4",
                task4_result=f"ERROR: DES key plaintext phải là 8 ký tự ASCII (8 bytes). Bạn đang nhập {len(key)} bytes.",
                task4_iv="",
            )
    else:
        # Key format là hex
        key_hex = "".join(key_input.split())

        if len(key_hex) != 16:
            return render_template(
                "index.html",
                active_tab="task4",
                task4_result=f"ERROR: DES key phải là 16 ký tự hex (8 bytes). Bạn đang nhập {len(key_hex)} ký tự.",
                task4_iv="",
            )

        try:
            key = bytes.fromhex(key_hex)
        except ValueError:
            return render_template(
                "index.html",
                active_tab="task4",
                task4_result=f"ERROR: Key không hợp lệ. Chỉ chấp nhận ký tự hex (0-9, A-F). Bạn nhập: '{key_hex}'",
                task4_iv="",
            )

    # IV (nếu có) - chỉ chấp nhận hex
    iv = None
    if iv_hex.strip():
        iv_hex_clean = "".join(iv_hex.split())

        if len(iv_hex_clean) != 16:
            return render_template(
                "index.html",
                active_tab="task4",
                task4_result=f"ERROR: DES IV phải là 16 ký tự hex (8 bytes). Bạn đang nhập {len(iv_hex_clean)} ký tự.",
                task4_iv="",
            )

        try:
            iv = bytes.fromhex(iv_hex_clean)
        except ValueError:
            return render_template(
                "index.html",
                active_tab="task4",
                task4_result=f"ERROR: IV không hợp lệ. Chỉ chấp nhận ký tự hex (0-9, A-F).",
                task4_iv="",
            )

    # Nếu dùng CBC mà không có IV => lỗi (bắt buộc cho cả encrypt và decrypt)
    if mode.upper() != "ECB" and iv is None:
        return render_template(
            "index.html",
            active_tab="task4",
            task4_result="ERROR: IV is required for CBC mode. Please enter a 16-character hex IV.",
            task4_iv="",
        )

    try:
        if action == "encrypt":
            ciphertext, used_iv = des_encrypt(data, key, mode.upper(), iv)
            result_output = ciphertext.hex()
            iv_hex_out = (
                used_iv.hex() if used_iv is not None else (iv.hex() if iv else "")
            )
        else:
            plaintext = des_decrypt(data, key, mode.upper(), iv)
            # Trả về plaintext dạng text (UTF-8) thay vì hex
            try:
                result_output = plaintext.decode("utf-8")
            except UnicodeDecodeError:
                # Nếu không decode được, trả về hex
                result_output = f"[Binary data - hex]: {plaintext.hex()}"
            iv_hex_out = iv.hex() if iv else ""
    except ValueError as e:
        error_str = str(e)
        if "padding" in error_str.lower():
            result_output = f"ERROR: {e}\n\nGợi ý: Key hoặc IV có thể không đúng. Lưu ý: Ngay cả khi key sai, đôi khi vẫn decrypt được nhưng kết quả sẽ là dữ liệu vô nghĩa."
        else:
            result_output = f"ERROR: {e}"
        iv_hex_out = ""
    except Exception as e:
        result_output = f"ERROR during DES {action}: {e}"
        iv_hex_out = ""

    return render_template(
        "index.html",
        active_tab="task4",
        task4_result=result_output,
        task4_iv=iv_hex_out,
    )


# ====================
# TASK 5 – AES
# ====================
@app.route("/task5/aes", methods=["POST"])
def task5_aes():
    file = request.files.get("input_file")
    plaintext_input = request.form.get("plaintext_input") or ""
    mode = request.form.get("mode")
    action = request.form.get("action")
    key_hex = request.form.get("key") or ""
    iv_hex = request.form.get("iv") or ""

    if not mode or not action or not key_hex:
        return redirect(url_for("index"))

    # Xử lý input
    data = None
    if plaintext_input.strip():
        if action == "decrypt":
            # Decrypt: input phải là hex
            hex_text = "".join(plaintext_input.split())
            try:
                data = bytes.fromhex(hex_text)
            except ValueError:
                return render_template(
                    "index.html",
                    active_tab="task5",
                    task5_result="ERROR: Khi decrypt, input phải là hex. Paste ciphertext hex vào ô textarea.",
                    task5_iv="",
                )
        else:
            # Encrypt: input là plaintext
            data = plaintext_input.encode("utf-8")
    elif file and file.filename:
        file_content = file.read().decode("utf-8", errors="ignore")

        if action == "decrypt":
            # Decrypt: file phải chứa hex
            hex_text = "".join(file_content.split())
            try:
                data = bytes.fromhex(hex_text)
            except ValueError:
                return render_template(
                    "index.html",
                    active_tab="task5",
                    task5_result="ERROR: Khi decrypt, file phải chứa chuỗi hex hợp lệ.",
                    task5_iv="",
                )
        else:
            # Encrypt: file chứa plaintext
            data = file_content.encode("utf-8")

    if data is None:
        return render_template(
            "index.html",
            active_tab="task5",
            task5_result="ERROR: Phải upload file hex HOẶC nhập vào textarea.",
            task5_iv="",
        )

    # Get key size (default to 128 if not specified)
    key_size = request.form.get("key_size", "128")

    # Key size mapping
    key_size_map = {
        "128": (32, 16, "AES-128"),
        "192": (48, 24, "AES-192"),
        "256": (64, 32, "AES-256"),
    }

    if key_size not in key_size_map:
        key_size = "128"  # Default fallback

    expected_hex_len, expected_bytes, aes_name = key_size_map[key_size]

    # Key validation - chấp nhận hex hoặc plaintext
    key_format = request.form.get("key_format") or "hex"
    key_input = request.form.get("key") or ""
    key_input = key_input.strip()

    if key_format == "plaintext":
        # Nếu là plaintext, chuyển thành bytes rồi kiểm tra độ dài
        key = key_input.encode("utf-8")
        if len(key) != expected_bytes:
            return render_template(
                "index.html",
                active_tab="task5",
                task5_result=f"ERROR: {aes_name} key plaintext phải là {expected_bytes} ký tự ASCII ({expected_bytes} bytes). Bạn đang nhập {len(key)} bytes.",
                task5_iv="",
            )
    else:
        # Key format là hex
        key_hex = "".join(key_input.split())
        if len(key_hex) != expected_hex_len:
            return render_template(
                "index.html",
                active_tab="task5",
                task5_result=f"ERROR: {aes_name} key phải là {expected_hex_len} ký tự hex ({expected_bytes} bytes). Bạn đang nhập {len(key_hex)} ký tự.",
                task5_iv="",
            )
        try:
            key = bytes.fromhex(key_hex)
        except ValueError:
            return render_template(
                "index.html",
                active_tab="task5",
                task5_result=f"ERROR: Key không hợp lệ. Chỉ chấp nhận ký tự hex (0-9, A-F). Bạn nhập: '{key_hex}'",
                task5_iv="",
            )

    # IV
    iv = None
    if iv_hex.strip():
        iv_hex_clean = "".join(iv_hex.split())

        # Validate IV length for AES (must be 32 hex chars = 16 bytes)
        if len(iv_hex_clean) != 32:
            return render_template(
                "index.html",
                active_tab="task5",
                task5_result=f"ERROR: AES IV phải là 32 ký tự hex (16 bytes). Bạn đang nhập {len(iv_hex_clean)} ký tự.",
                task5_iv="",
            )

        try:
            iv = bytes.fromhex(iv_hex_clean)
        except ValueError:
            return render_template(
                "index.html",
                active_tab="task5",
                task5_result="ERROR: IV không hợp lệ. Chỉ chấp nhận ký tự hex (0-9, A-F).",
                task5_iv="",
            )

    # CBC mode bắt buộc phải có IV (cả encrypt và decrypt)
    if mode.upper() != "ECB" and iv is None:
        return render_template(
            "index.html",
            active_tab="task5",
            task5_result="ERROR: IV is required for CBC mode. Please enter a 32-character hex IV.",
            task5_iv="",
        )

    try:
        if action == "encrypt":
            ciphertext, used_iv = aes_encrypt(data, key, mode.upper(), iv)
            result_output = ciphertext.hex()
            iv_hex_out = (
                used_iv.hex() if used_iv is not None else (iv.hex() if iv else "")
            )
        else:
            plaintext = aes_decrypt(data, key, mode.upper(), iv)
            # Trả về plaintext dạng text (UTF-8) thay vì hex
            try:
                result_output = plaintext.decode("utf-8")
            except UnicodeDecodeError:
                result_output = f"[Binary data - hex]: {plaintext.hex()}"
            iv_hex_out = iv.hex() if iv else ""
    except ValueError as e:
        error_str = str(e)
        if "padding" in error_str.lower():
            result_output = f"ERROR: {e}\n\nGợi ý: Key hoặc IV có thể không đúng. Lưu ý: Ngay cả khi key sai, đôi khi vẫn decrypt được nhưng kết quả sẽ là dữ liệu vô nghĩa."
        else:
            result_output = f"ERROR: {e}"
        iv_hex_out = ""
    except Exception as e:
        result_output = f"ERROR during AES {action}: {e}"
        iv_hex_out = ""

    return render_template(
        "index.html",
        active_tab="task5",
        task5_result=result_output,
        task5_iv=iv_hex_out,
    )


# ====================
# API ENDPOINTS (AJAX)
# ====================
@app.route("/api/task1/caesar", methods=["POST"])
def api_task1_caesar():
    """API endpoint for Caesar cipher breaking (AJAX)"""
    try:
        file = request.files.get("cipher_file")
        cipher_text = request.form.get("cipher_text") or ""

        # Process and validate input
        success, result = process_input(file, cipher_text)
        if not success:
            return jsonify({"success": False, "error": result}), 400

        ciphertext = result

        # Debug log
        print(f"[DEBUG] Ciphertext length: {len(ciphertext)}")
        print(f"[DEBUG] First 100 chars: {ciphertext[:100]}")

        # Gọi hàm giải Caesar
        key, plaintext = break_caesar(ciphertext)

        print(f"[DEBUG] Key found: {key}")

        return jsonify({"success": True, "key": key, "plaintext": plaintext})
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/task2/substitution", methods=["POST"])
def api_task2_substitution():
    """API endpoint for Substitution cipher breaking (AJAX)"""
    try:
        file = request.files.get("cipher_file")
        cipher_text = request.form.get("cipher_text") or ""

        # Process and validate input
        success, result = process_input(file, cipher_text)
        if not success:
            return jsonify({"success": False, "error": result}), 400

        ciphertext = result

        # Gọi hàm crack substitution
        score, mapping_str, plaintext = break_substitution(ciphertext)

        # Parse mapping_str để lấy plain alphabet
        # Format: "CIPHER: ABC... | PLAIN : XYZ..."
        plain_alphabet = mapping_str  # default

        if " | PLAIN : " in mapping_str:
            plain_alphabet = mapping_str.split(" | PLAIN : ")[-1].strip()
        elif " | plain : " in mapping_str:
            plain_alphabet = mapping_str.split(" | plain : ")[-1].strip()

        return jsonify(
            {
                "success": True,
                "score": score,
                "mapping": plain_alphabet.upper(),  # Chỉ trả plain alphabet
                "plaintext": plaintext,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/task3/vigenere", methods=["POST"])
def api_task3_vigenere():
    """API endpoint for Vigenere cipher breaking (AJAX)"""
    try:
        file = request.files.get("cipher_file")
        cipher_text = request.form.get("cipher_text") or ""

        # Process and validate input
        success, result = process_input(file, cipher_text)
        if not success:
            return jsonify({"success": False, "error": result}), 400

        ciphertext = result

        # Nhận 3 giá trị
        key, plaintext, score = break_vigenere(ciphertext)

        return jsonify(
            {"success": True, "key": key, "plaintext": plaintext, "score": score}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ====================
# CHATBOT - HYBRID (Offline Knowledge + Online AI)
# ====================
from crypto.chatbot_knowledge import get_response as get_offline_response


@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    """
    Chatbot endpoint - Hybrid approach:
    1. Try offline knowledge base first (instant, always works)
    2. Fallback to Gemini AI if available
    """
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"success": False, "error": "Message is required"}), 400

        # STEP 1: Try offline knowledge base first
        offline_response = get_offline_response(user_message)

        # If offline has confident answer (not the fallback "??" message), use it immediately
        if offline_response and not offline_response.lstrip().startswith("??"):
            return jsonify(
                {
                    "success": True,
                    "response": offline_response
                    + "\n\n_?? Powered by Offline Knowledge Base_",
                }
            )

        # STEP 2: Offline doesn't have answer, try Gemini API if available
        if not GEMINI_API_KEY:
            # No API key, return offline fallback
            return jsonify(
                {
                    "success": True,
                    "response": offline_response
                    + "\n\n_⚠️ Chế độ Offline - API key chưa cấu hình_",
                }
            )

        # Try Gemini API for complex questions

        # System prompt for cryptography assistant - TIẾNG VIỆT
        system_prompt = """Bạn là trợ lý mật mã học thông minh cho dự án Lab06 - Thuật Toán Mã Hóa. 
Nhiệm vụ của bạn là giúp người dùng hiểu về:
- Mã cổ điển (Caesar, Substitution, Vigenère)
- Thuật toán mã hóa hiện đại (DES, AES)
- Kỹ thuật phân tích mật mã (cryptanalysis)
- Các chế độ block cipher (ECB, CBC)
- Best practices trong mật mã học

TRẢ LỜI BẰNG TIẾNG VIỆT. Giải thích rõ ràng, súc tích, mang tính giáo dục. Dùng ví dụ khi cần thiết.
Nếu hỏi về implementation, hãy đề cập đến các thuật toán cụ thể trong project này.
Dùng emoji phù hợp để làm câu trả lời sinh động hơn."""

        # Call Gemini REST API with retry logic
        # Try different models (all are available in v1beta)
        models = ["gemini-flash-latest", "gemini-2.5-flash", "gemini-2.0-flash-exp"]

        headers = {"Content-Type": "application/json"}

        payload = {
            "contents": [
                {"parts": [{"text": f"{system_prompt}\n\nUser: {user_message}"}]},
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,  # Increased for longer responses
                "topP": 0.9,
                "topK": 40,
            },
        }

        # Retry logic for rate limiting
        max_retries = 2
        retry_delay = 2  # seconds

        last_error = None

        # Try different models
        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

            for attempt in range(max_retries):
                try:
                    response = requests.post(
                        url, headers=headers, json=payload, timeout=30
                    )

                    # If rate limited, try next model
                    if response.status_code == 429:
                        last_error = f"Rate limit: {model}"
                        break  # Try next model

                    # If model not found, try next
                    if response.status_code == 404:
                        last_error = f"Model not available: {model}"
                        break

                    response.raise_for_status()
                    result = response.json()

                    # Extract text from response
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            text = candidate["content"]["parts"][0].get("text", "")
                            return jsonify(
                                {
                                    "success": True,
                                    "response": text
                                    + "\n\n_🤖 Powered by Google Gemini AI_",
                                }
                            )

                    last_error = "No valid response"
                    break

                except requests.exceptions.Timeout:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    last_error = "Timeout"
                    break
                except requests.exceptions.RequestException as e:
                    last_error = str(e)
                    break

        # All models failed - fallback to offline
        return jsonify(
            {
                "success": True,
                "response": offline_response
                + f"\n\n_⚠️ Gemini API không khả dụng (Lỗi: {last_error}).\n"
                + "Sử dụng chế độ Offline Knowledge Base._",
            }
        )

    except Exception as e:
        # Ultimate fallback - always return offline response
        try:
            offline_resp = get_offline_response(user_message)
            return jsonify(
                {
                    "success": True,
                    "response": offline_resp + f"\n\n_⚠️ Lỗi hệ thống: {str(e)}_",
                }
            )
        except:
            return jsonify({"success": False, "error": f"System error: {str(e)}"}), 500


if __name__ == "__main__":
    # debug=True chỉ nên dùng khi dev
    app.run(debug=True)
