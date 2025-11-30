# crypto/caesar.py
"""
Caesar Cipher Breaker (Best Version)
------------------------------------
- Giải mã Caesar bằng brute-force 26 khóa
- Chấm điểm plaintext bằng CHI-SQUARE statistic (mạnh hơn tần suất thô)
- Tương thích hoàn toàn với backend Flask:
      from crypto.caesar import break_caesar
- Giữ nguyên mọi ký tự không phải chữ cái (space, number, punctuation)
"""

import string

# Tần suất chữ cái tiếng Anh chuẩn (%)
ENGLISH_FREQ = {
    "A": 8.17,
    "B": 1.49,
    "C": 2.78,
    "D": 4.25,
    "E": 12.70,
    "F": 2.23,
    "G": 2.02,
    "H": 6.09,
    "I": 6.97,
    "J": 0.15,
    "K": 0.77,
    "L": 4.03,
    "M": 2.41,
    "N": 6.75,
    "O": 7.51,
    "P": 1.93,
    "Q": 0.10,
    "R": 5.99,
    "S": 6.33,
    "T": 9.06,
    "U": 2.76,
    "V": 0.98,
    "W": 2.36,
    "X": 0.15,
    "Y": 1.97,
    "Z": 0.07,
}

LETTERS = string.ascii_uppercase


def shift_char(c: str, k: int) -> str:
    """
    Dịch 1 ký tự theo khóa k (0–25). Giữ nguyên ký tự không phải chữ cái.
    """
    if c.isalpha():
        if c.isupper():
            return chr((ord(c) - ord("A") - k) % 26 + ord("A"))
        else:
            return chr((ord(c) - ord("a") - k) % 26 + ord("a"))
    return c


def decrypt_caesar_with_key(ciphertext: str, k: int) -> str:
    """
    Trả về plaintext khi giải mã ciphertext bằng key k.
    KHÔNG bao giờ trả về None.
    """
    return "".join(shift_char(c, k) for c in ciphertext)


def chi_square_score(text: str) -> float:
    """
    Tính chi-square statistic giữa phân bố chữ cái của text và phân bố
    tiếng Anh chuẩn. Chi-square càng nhỏ -> càng giống tiếng Anh.
    """
    if text is None:
        return float("inf")

    text = text.upper()
    counts = {ch: 0 for ch in LETTERS}
    total_letters = 0

    for c in text:
        if c in LETTERS:
            counts[c] += 1
            total_letters += 1

    # Nếu không có chữ cái nào thì coi như rất tệ
    if total_letters == 0:
        return float("inf")

    chi_sq = 0.0
    for ch in LETTERS:
        observed = counts[ch]
        expected = ENGLISH_FREQ[ch] * total_letters / 100
        chi_sq += (observed - expected) ** 2 / expected

    return chi_sq


def break_caesar(ciphertext: str):
    """
    Bruteforce 26 khóa, chấm điểm từng plaintext bằng chi-square.
    Trả về (best_key, best_plaintext).
    """
    best_key = 0
    best_plain = ""
    best_score = float("inf")  # chi-square càng nhỏ càng tốt

    # Đảm bảo ciphertext là string
    if ciphertext is None:
        ciphertext = ""

    for k in range(26):
        plain = decrypt_caesar_with_key(ciphertext, k)
        score = chi_square_score(plain)

        if score < best_score:
            best_score = score
            best_key = k
            best_plain = plain

    return best_key, best_plain
