# crypto/caesar.py
"""
Caesar Cipher Breaker (Optimized Version)
------------------------------------------
- Giải mã Caesar bằng brute-force 26 khóa
- Chấm điểm plaintext bằng CHI-SQUARE statistic (mạnh hơn tần suất thô)
- Tương thích hoàn toàn với backend Flask:
      from crypto.caesar import break_caesar
- Giữ nguyên mọi ký tự không phải chữ cái (space, number, punctuation)

"""

import string

# Tần suất chữ cái tiếng Anh chuẩn (%) - converted to decimal
ENGLISH_FREQ = {
    "A": 0.0817,
    "B": 0.0149,
    "C": 0.0278,
    "D": 0.0425,
    "E": 0.1270,
    "F": 0.0223,
    "G": 0.0202,
    "H": 0.0609,
    "I": 0.0697,
    "J": 0.0015,
    "K": 0.0077,
    "L": 0.0403,
    "M": 0.0241,
    "N": 0.0675,
    "O": 0.0751,
    "P": 0.0193,
    "Q": 0.0010,
    "R": 0.0599,
    "S": 0.0633,
    "T": 0.0906,
    "U": 0.0276,
    "V": 0.0098,
    "W": 0.0236,
    "X": 0.0015,
    "Y": 0.0197,
    "Z": 0.0007,
}

LETTERS = string.ascii_uppercase
LETTERS_SET = set(LETTERS)  # For faster membership testing


def shift_char(c: str, k: int) -> str:
    """
    Dịch 1 ký tự theo khóa k (0–25). Giữ nguyên ký tự không phải chữ cái.
    Optimized: reduced branching, direct calculation.
    """
    if not c.isalpha():
        return c

    base = ord("A") if c.isupper() else ord("a")
    return chr((ord(c) - base - k) % 26 + base)


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

    Optimized: faster counting, reduced operations.
    """
    if not text:
        return float("inf")

    # Count letters efficiently using list (faster than dict for 26 items)
    counts = [0] * 26
    total = 0

    for c in text.upper():
        if c in LETTERS_SET:
            counts[ord(c) - 65] += 1
            total += 1

    if total == 0:
        return float("inf")

    # Calculate chi-square with pre-computed frequencies
    chi_sq = 0.0
    for i, letter in enumerate(LETTERS):
        observed = counts[i]
        expected = ENGLISH_FREQ[letter] * total
        if expected > 0:  # Avoid division by zero
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


# ===================== CLI Mode (theo đúng format đề bài) ===================== #


def _run_cli():
    """
    CLI cho Task 1 - Caesar cipher breaker

    Usage:
        python -m crypto.caesar -i data/ciphertext.txt -o output_task1.txt

    Output format:
        - Dòng 1: khóa k
        - Dòng 2+: plaintext
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Task 1 - Caesar cipher breaker (brute-force + chi-square)"
    )
    parser.add_argument("-i", "--input", required=True, help="File ciphertext input")
    parser.add_argument("-o", "--output", required=True, help="File plaintext output")
    args = parser.parse_args()

    # Đọc ciphertext
    with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
        ciphertext = f.read()

    # Break cipher
    key, plaintext = break_caesar(ciphertext)

    # Ghi output theo format đề bài
    with open(args.output, "w", encoding="utf-8", errors="ignore") as out:
        out.write(str(key) + "\n")
        out.write(plaintext)

    print(f"[+] Caesar cipher cracked!")
    print(f"[+] Key found: {key}")
    print(f"[+] Output written to: {args.output}")


if __name__ == "__main__":
    _run_cli()
