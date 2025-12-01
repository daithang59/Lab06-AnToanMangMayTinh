# crypto/vigenere.py
"""
Task 3 - Vigenère cipher breaker (dùng Index of Coincidence + chi-square)

- Không biết trước độ dài khóa.
- Bước 1: Dùng Index of Coincidence (IC) để ước lượng một số độ dài khóa ứng viên.
- Bước 2: Với mỗi độ dài khóa ứng viên:
    + Chia ciphertext thành các "Caesar-subsets".
    + Giải từng subset bằng phân tích tần suất (chi-square).
- Bước 3: Chọn key cho ra plaintext tiếng Anh nhất (chi-square nhỏ nhất).

Public API cho Flask:
    from crypto.vigenere import break_vigenere
    key, plaintext, score = break_vigenere(ciphertext)

CLI:
    python -m crypto.vigenere -i data/cipher.txt -o output_task3.txt

    output_task3.txt:
        dòng 1: khóa (key) tìm được
        dòng 2+: plaintext
"""

import string
import random

ALPHABET = string.ascii_uppercase

# Tần suất chữ cái tiếng Anh chuẩn
ENGLISH_FREQ = {
    "A": 0.08167,
    "B": 0.01492,
    "C": 0.02782,
    "D": 0.04253,
    "E": 0.12702,
    "F": 0.02228,
    "G": 0.02015,
    "H": 0.06094,
    "I": 0.06966,
    "J": 0.00153,
    "K": 0.00772,
    "L": 0.04025,
    "M": 0.02406,
    "N": 0.06749,
    "O": 0.07507,
    "P": 0.01929,
    "Q": 0.00095,
    "R": 0.05987,
    "S": 0.06327,
    "T": 0.09056,
    "U": 0.02758,
    "V": 0.00978,
    "W": 0.02360,
    "X": 0.00150,
    "Y": 0.01974,
    "Z": 0.00074,
}


# ===================== 1. Mã hóa / giải mã cơ bản ======================= #


def encrypt_vigenere(plaintext: str, key: str) -> str:
    """
    Vigenère chuẩn: C = P + K (mod 26).
    Dùng cho test / demo, không dùng trong solver chính.
    """
    key = key.upper()
    res = []
    ki = 0
    for ch in plaintext:
        if ch.isalpha():
            base = "A" if ch.isupper() else "a"
            p = ord(ch.upper()) - ord("A")
            k = ord(key[ki % len(key)]) - ord("A")
            c = (p + k) % 26
            res.append(chr(ord(base) + c))
            ki += 1
        else:
            res.append(ch)
    return "".join(res)


def decrypt_vigenere(ciphertext: str, key: str) -> str:
    """
    Giải mã Vigenère chuẩn: P = C - K (mod 26).
    Chỉ dịch A–Z/a–z, giữ nguyên ký tự khác, bảo toàn hoa/thường.
    """
    key = key.upper()
    res = []
    ki = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = "A" if ch.isupper() else "a"
            c = ord(ch.upper()) - ord("A")
            k = ord(key[ki % len(key)]) - ord("A")
            p = (c - k) % 26
            res.append(chr(ord(base) + p))
            ki += 1
        else:
            res.append(ch)
    return "".join(res)


# ========================= 2. Index of Coincidence ======================= #


def _index_of_coincidence(seq: str) -> float:
    """IC cho chuỗi seq (chỉ gồm A-Z)."""
    N = len(seq)
    if N <= 1:
        return 0.0
    counts = [0] * 26
    for ch in seq:
        if ch in ALPHABET:
            counts[ord(ch) - 65] += 1
    numerator = sum(c * (c - 1) for c in counts)
    return numerator / (N * (N - 1))


def _guess_key_lengths_by_ic(letters: str, max_key_len: int = 20, top_k: int = 7):
    """
    Dùng Index of Coincidence để ước lượng các độ dài khóa tiềm năng.

    Với mỗi key_len:
        - Chia letters thành key_len subset: vị trí i, i+k, i+2k, ...
        - Tính IC của từng subset, lấy trung bình.
    IC càng cao (gần IC tiếng Anh ~0.065) thì key_len càng có khả năng đúng.

    Trả về list (key_len, avg_ic) đã sort giảm dần theo avg_ic, lấy top_k.
    """
    candidates = []

    for key_len in range(2, max_key_len + 1):  # bỏ key_len = 1 (Caesar)
        ics = []
        for i in range(key_len):
            subset = letters[i::key_len]
            if len(subset) > 1:
                ics.append(_index_of_coincidence(subset))
        if not ics:
            continue
        avg_ic = sum(ics) / len(ics)
        candidates.append((key_len, avg_ic))

    candidates.sort(key=lambda x: -x[1])  # avg_ic lớn hơn → tốt hơn
    return candidates[:top_k]


# ======================== 3. Phân tích tần suất Caesar =================== #


def _best_shift_for_subset(subset: str) -> int:
    """
    subset: chuỗi chỉ gồm A-Z, thuộc về 1 vị trí khóa.
    Tìm shift (0..25) sao cho chi-square so với ENGLISH_FREQ là nhỏ nhất.
    shift chính là giá trị key-letter (A=0, B=1, ...).
    """
    N = len(subset)
    if N == 0:
        return 0

    best_shift = 0
    best_chi = float("inf")

    for shift in range(26):
        counts = [0] * 26
        for ch in subset:
            c = ord(ch) - 65
            # P = C - K, ở đây shift = K
            p = (c - shift) % 26
            counts[p] += 1

        chi = 0.0
        for i, obs in enumerate(counts):
            expected = ENGLISH_FREQ[ALPHABET[i]] * N
            if expected > 0:
                chi += (obs - expected) ** 2 / expected

        if chi < best_chi:
            best_chi = chi
            best_shift = shift

    return best_shift


# =========================== 4. Scoring plaintext ======================== #


def _chi_square_text(text: str) -> float:
    """Chi-square của toàn bộ plaintext (so với ENGLISH_FREQ)."""
    counts = [0] * 26
    N = 0
    for ch in text.upper():
        if ch in ALPHABET:
            counts[ord(ch) - 65] += 1
            N += 1

    if N == 0:
        return float("inf")

    chi = 0.0
    for i, obs in enumerate(counts):
        expected = ENGLISH_FREQ[ALPHABET[i]] * N
        if expected > 0:
            chi += (obs - expected) ** 2 / expected
    return chi


# ========================== 5. Solver chính ============================== #


def _break_vigenere_internal(ciphertext: str, max_key_len: int = 20, top_k: int = 7):
    """
    Solver chinh:
    - Lay chuoi letters = chi cac chu cai A-Z tu ciphertext.
    - Dung IC de chon ra mot so do dai khoa ung vien (top_k).
    - Moi key_len ung vien:
        + Chia letters thanh key_len subset.
        + Moi subset giai bang chi-square -> 1 ky tu khoa.
        + Ghep thanh key, giai toan ciphertext, tinh chi-square toan cuc.
    - Chon key co chi-square nho nhat.
    """
    letters = ''.join(ch for ch in ciphertext.upper() if ch in ALPHABET)
    if len(letters) < 20:
        # too short to guess reliably
        return 'A', decrypt_vigenere(ciphertext, 'A'), float('inf')

    candidates = _guess_key_lengths_by_ic(letters, max_key_len, top_k)

    best_key = None
    best_plain = None
    best_score = float('inf')

    for key_len, avg_ic in candidates:
        shifts = []
        for i in range(key_len):
            subset = ''.join(letters[j] for j in range(i, len(letters), key_len))
            shift = _best_shift_for_subset(subset)
            shifts.append(shift)

        key = ''.join(ALPHABET[s] for s in shifts)
        plain = decrypt_vigenere(ciphertext, key)

        chi = _chi_square_text(plain)
        if chi < best_score:
            best_score = chi
            best_key = key
            best_plain = plain

    if best_key is not None:
        best_key = _reduce_repeating_key(best_key)
        best_plain = decrypt_vigenere(ciphertext, best_key)

    return best_key, best_plain, best_score



def break_vigenere(ciphertext: str):
    """
    Hàm public dùng trong Flask.

    Trả về:
        key (str): khóa Vigenère (A-Z).
        plaintext (str): ciphertext đã giải.
        score (float): chi-square (càng nhỏ càng giống tiếng Anh).
    """
    random.seed()
    return _break_vigenere_internal(ciphertext, max_key_len=20, top_k=7)


# ========================= Utility functions ============================= #


def _reduce_repeating_key(key: str) -> str:
    """
    Nếu key là lặp lại của một mẫu ngắn hơn (ví dụ 'SECURITYSECURITY'),
    trả về mẫu ngắn nhất ('SECURITY').
    Nếu không phải lặp, trả về key như cũ.
    """
    n = len(key)
    for p in range(1, n + 1):
        if n % p == 0:
            pattern = key[:p]
            if pattern * (n // p) == key:
                return pattern
    return key


# ============================== 6. CLI mode ============================== #


def _run_cli():
    """
    Chạy từ command line, đúng format đề:
        dòng 1: khóa k
        dòng 2+: plaintext
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Task 3 - Vigenère cipher breaker (IC + chi-square)"
    )
    parser.add_argument("-i", "--input", required=True, help="File ciphertext input")
    parser.add_argument("-o", "--output", required=True, help="File plaintext output")
    parser.add_argument(
        "--max-key",
        type=int,
        default=20,
        help="Độ dài khóa tối đa để thử (mặc định 20)",
    )
    parser.add_argument(
        "--top-k", type=int, default=7, help="Số độ dài khóa ứng viên (mặc định 7)"
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
        ciphertext = f.read()

    key, plaintext, score = _break_vigenere_internal(
        ciphertext,
        max_key_len=args.max_key,
        top_k=args.top_k,
    )

    with open(args.output, "w", encoding="utf-8", errors="ignore") as out:
        out.write(key + "\n")
        out.write(plaintext)

    print(f"[+] Best key  : {key}")
    print(f"[+] Chi-square: {score:.2f}")


if __name__ == "__main__":
    _run_cli()
