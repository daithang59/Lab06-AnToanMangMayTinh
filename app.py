from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os

# Import các module crypto bạn sẽ tự cài đặt
from crypto.caesar import break_caesar
from crypto.substitution import break_substitution
from crypto.vigenere import break_vigenere
from crypto.des_modes import des_encrypt, des_decrypt
from crypto.aes_modes import aes_encrypt, aes_decrypt
from crypto.charset_filter import validate_and_filter

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "change-this-secret-key"  # nếu sau này bạn dùng flash, session, v.v.
)

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

    return render_template(
        "index.html",
        active_tab="task2",
        task2_score=score,
        task2_mapping=mapping_str,
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

    # Key - chỉ chấp nhận hex
    key_hex = "".join(key_hex.split())

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

    # Nếu dùng CBC và decrypt mà không có IV => lỗi
    if mode.upper() != "ECB" and action == "decrypt" and iv is None:
        return render_template(
            "index.html",
            active_tab="task4",
            task4_result="ERROR: IV is required for this mode when decrypting.",
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

    # Key validation
    key_hex = "".join(key_hex.split())
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
        try:
            iv = bytes.fromhex(iv_hex_clean)
        except ValueError:
            return render_template(
                "index.html",
                active_tab="task5",
                task5_result="ERROR: Invalid hex in IV.",
                task5_iv="",
            )

    # CBC decrypt cần IV
    if mode.upper() != "ECB" and action == "decrypt" and iv is None:
        return render_template(
            "index.html",
            active_tab="task5",
            task5_result="ERROR: IV is required for this mode when decrypting.",
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

        # Gọi hàm giải Caesar
        key, plaintext = break_caesar(ciphertext)

        return jsonify({"success": True, "key": key, "plaintext": plaintext})
    except Exception as e:
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

        return jsonify(
            {
                "success": True,
                "score": score,
                "mapping": mapping_str,
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


if __name__ == "__main__":
    # debug=True chỉ nên dùng khi dev
    app.run(debug=True)
