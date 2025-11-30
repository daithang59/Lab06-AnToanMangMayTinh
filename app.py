from flask import Flask, render_template, request, redirect, url_for

# Import các module crypto bạn sẽ tự cài đặt
from crypto.caesar import break_caesar
from crypto.substitution import break_substitution
from crypto.vigenere import break_vigenere
from crypto.des_modes import des_encrypt, des_decrypt
from crypto.aes_modes import aes_encrypt, aes_decrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"  # nếu sau này bạn dùng flash, session, v.v.


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
    if not file:
        return redirect(url_for("index"))

    # Đọc ciphertext (UTF-8 text)
    ciphertext = file.read().decode("utf-8", errors="ignore")

    # Gọi hàm giải Caesar
    key, plaintext = break_caesar(ciphertext)

    return render_template(
        "index.html",
        active_tab="task1",
        task1_key=key,
        task1_result=plaintext,
    )


# ====================
# TASK 2 – SUBSTITUTION
# ====================
@app.route("/task2/substitution", methods=["POST"])
def task2_substitution():
    file = request.files.get("cipher_file")
    if not file:
        return redirect(url_for("index"))

    ciphertext = file.read().decode("utf-8", errors="ignore")

    # Gọi hàm crack substitution
    score, mapping_str, plaintext = break_substitution(ciphertext)

    return render_template(
        "index.html",
        active_tab="task2",
        task2_score=score,
        task2_mapping=mapping_str,
        task2_result=plaintext,
    )


# ====================
# TASK 3 – VIGENERE
# ====================
@app.route("/task3/vigenere", methods=["POST"])
def task3_vigenere():
    file = request.files.get("cipher_file")
    if not file:
        return redirect(url_for("index"))

    ciphertext = file.read().decode("utf-8", errors="ignore")

    # Gọi hàm crack Vigenère
    key, plaintext = break_vigenere(ciphertext)

    return render_template(
        "index.html",
        active_tab="task3",
        task3_key=key,
        task3_result=plaintext,
    )


# ====================
# TASK 4 – DES
# ====================
@app.route("/task4/des", methods=["POST"])
def task4_des():
    file = request.files.get("input_file")
    mode = request.form.get("mode")        # 'ECB' hoặc 'CBC' ...
    action = request.form.get("action")    # 'encrypt' hoặc 'decrypt'
    key_hex = request.form.get("key") or ""
    iv_hex = request.form.get("iv") or ""

    if not file or not mode or not action or not key_hex:
        return redirect(url_for("index"))

    # Đọc dữ liệu hex từ file
    hex_text = file.read().decode("utf-8", errors="ignore")
    hex_text = "".join(hex_text.split())  # bỏ whitespace/newline
    try:
        data = bytes.fromhex(hex_text)
    except ValueError:
        # Nếu hex không hợp lệ, trả về giao diện với thông báo đơn giản
        return render_template(
            "index.html",
            active_tab="task4",
            task4_result="ERROR: Invalid hex in input file.",
            task4_iv="",
        )

    # Key
    key_hex = "".join(key_hex.split())
    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        return render_template(
            "index.html",
            active_tab="task4",
            task4_result="ERROR: Invalid hex in key.",
            task4_iv="",
        )

    # IV (nếu có)
    iv = None
    if iv_hex.strip():
        iv_hex_clean = "".join(iv_hex.split())
        try:
            iv = bytes.fromhex(iv_hex_clean)
        except ValueError:
            return render_template(
                "index.html",
                active_tab="task4",
                task4_result="ERROR: Invalid hex in IV.",
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
            result_hex = ciphertext.hex()
            iv_hex_out = used_iv.hex() if used_iv is not None else (iv.hex() if iv else "")
        else:
            plaintext = des_decrypt(data, key, mode.upper(), iv)
            result_hex = plaintext.hex()
            iv_hex_out = iv.hex() if iv else ""
    except Exception as e:
        result_hex = f"ERROR during DES {action}: {e}"
        iv_hex_out = ""

    return render_template(
        "index.html",
        active_tab="task4",
        task4_result=result_hex,
        task4_iv=iv_hex_out,
    )


# ====================
# TASK 5 – AES
# ====================
@app.route("/task5/aes", methods=["POST"])
def task5_aes():
    file = request.files.get("input_file")
    mode = request.form.get("mode")
    action = request.form.get("action")
    key_hex = request.form.get("key") or ""
    iv_hex = request.form.get("iv") or ""

    if not file or not mode or not action or not key_hex:
        return redirect(url_for("index"))

    # Đọc dữ liệu hex từ file
    hex_text = file.read().decode("utf-8", errors="ignore")
    hex_text = "".join(hex_text.split())
    try:
        data = bytes.fromhex(hex_text)
    except ValueError:
        return render_template(
            "index.html",
            active_tab="task5",
            task5_result="ERROR: Invalid hex in input file.",
            task5_iv="",
        )

    # Key
    key_hex = "".join(key_hex.split())
    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        return render_template(
            "index.html",
            active_tab="task5",
            task5_result="ERROR: Invalid hex in key.",
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
            result_hex = ciphertext.hex()
            iv_hex_out = used_iv.hex() if used_iv is not None else (iv.hex() if iv else "")
        else:
            plaintext = aes_decrypt(data, key, mode.upper(), iv)
            result_hex = plaintext.hex()
            iv_hex_out = iv.hex() if iv else ""
    except Exception as e:
        result_hex = f"ERROR during AES {action}: {e}"
        iv_hex_out = ""

    return render_template(
        "index.html",
        active_tab="task5",
        task5_result=result_hex,
        task5_iv=iv_hex_out,
    )


if __name__ == "__main__":
    # debug=True chỉ nên dùng khi dev
    app.run(debug=True)
