# crypto/vigenere.py
"""
Task 3 - Vigenère cipher breaker (dùng Index of Coincidence + chi-square)

- Không biết trước độ dài khóa.
- Bước 1: Dùng Index of Coincidence (IC) để ước lượng một số độ dài khóa ứng viên.
- Bước 2: Với mỗi độ dài khóa ứng viên:
    + Chia ciphertext thành các "Caesar-subsets".
    + Giải từng subset bằng phân tích tần suất (chi-square).
- Bước 3: Chọn key cho ra plaintext tiếng Anh nhất (chi-square nhỏ nhất).
"""

import string
import random

ALPHABET = string.ascii_uppercase
ALPHABET_SET = set(ALPHABET)  # For faster membership testing

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
    """
    IC cho chuỗi seq (chỉ gồm A-Z).
    Optimized: faster counting with list, reduced operations.
    """
    N = len(seq)
    if N <= 1:
        return 0.0

    counts = [0] * 26
    for ch in seq:
        if ch in ALPHABET_SET:
            counts[ord(ch) - 65] += 1

    # Calculate IC efficiently
    numerator = sum(c * (c - 1) for c in counts)
    return numerator / (N * (N - 1))


def _guess_key_lengths_by_ic(letters: str, max_key_len: int = 30, top_k: int = 10):
    """
    Dùng Index of Coincidence để ước lượng các độ dài khóa tiềm năng.

    Với mỗi key_len:
        - Chia letters thành key_len subset: vị trí i, i+k, i+2k, ...
        - Tính IC của từng subset, lấy trung bình.
    IC càng cao (gần IC tiếng Anh ~0.065) thì key_len càng có khả năng đúng.

    Trả về list (key_len, avg_ic) đã sort giảm dần theo avg_ic, lấy top_k.

    Optimized: list comprehension, reduced allocations.
    """
    candidates = []
    letters_len = len(letters)

    for key_len in range(2, min(max_key_len + 1, letters_len // 4)):
        # Calculate IC for all subsets
        ics = [
            _index_of_coincidence(letters[i::key_len])
            for i in range(key_len)
            if len(letters[i::key_len]) > 1
        ]

        if ics:
            avg_ic = sum(ics) / len(ics)
            candidates.append((key_len, avg_ic))

    # Sort by IC (higher is better) and return top_k
    candidates.sort(key=lambda x: -x[1])
    return candidates[:top_k]


# ======================== 3. Phân tích tần suất Caesar =================== #


def _best_shift_for_subset(subset: str) -> int:
    """
    subset: chuỗi chỉ gồm A-Z, thuộc về 1 vị trí khóa.
    Tìm shift (0..25) sao cho chi-square so với ENGLISH_FREQ là nhỏ nhất.
    shift chính là giá trị key-letter (A=0, B=1, ...).

    Optimized: reduced memory allocations, faster calculation.
    """
    N = len(subset)
    if N == 0:
        return 0

    best_shift = 0
    best_chi = float("inf")

    # Pre-convert subset to indices for faster processing
    subset_indices = [ord(ch) - 65 for ch in subset if ch in ALPHABET_SET]
    N = len(subset_indices)

    for shift in range(26):
        counts = [0] * 26
        for idx in subset_indices:
            counts[(idx - shift) % 26] += 1

        # Calculate chi-square
        chi = sum(
            (obs - ENGLISH_FREQ[ALPHABET[i]] * N) ** 2 / (ENGLISH_FREQ[ALPHABET[i]] * N)
            for i, obs in enumerate(counts)
            if ENGLISH_FREQ[ALPHABET[i]] > 0
        )

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


def _break_vigenere_internal(ciphertext: str, max_key_len: int = 30, top_k: int = 10):
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
    print("\n" + "=" * 60)
    print("[TASK 3] BẮT ĐẦU PHÁ MÃ VIGENÈRE CIPHER")
    print("=" * 60)
    print(f"Độ dài ciphertext: {len(ciphertext)} ký tự")
    print("Phương pháp: Index of Coincidence + Chi-square")
    print("-" * 60)

    letters = "".join(ch for ch in ciphertext.upper() if ch in ALPHABET)
    print(f"Số chữ cái (A-Z): {len(letters)}")

    if len(letters) < 20:
        # too short to guess reliably
        print("⚠ CẢNH BÁO: Ciphertext quá ngắn, không thể phân tích chính xác")
        return "A", decrypt_vigenere(ciphertext, "A"), float("inf")

    print("\nBƯỚC 1: Tính Index of Coincidence để ước lượng độ dài khóa...")
    candidates = _guess_key_lengths_by_ic(letters, max_key_len, top_k)

    print(f"\nCác độ dài khóa ứng viên (top {top_k}):")
    for i, (klen, ic) in enumerate(candidates, 1):
        print(f"  {i}. Key length = {klen:2d}, IC = {ic:.4f}")

    print("\nBƯỚC 2: Thử giải mã với từng độ dài khóa...")
    print("-" * 60)

    best_key = None
    best_plain = None
    best_score = float("inf")

    for idx, (key_len, ic_val) in enumerate(candidates, 1):
        print(
            f"\n[{idx}/{len(candidates)}] Thử key length = {key_len} (IC={ic_val:.4f})"
        )
        shifts = []
        for i in range(key_len):
            subset = "".join(letters[j] for j in range(i, len(letters), key_len))
            shift = _best_shift_for_subset(subset)
            shifts.append(shift)
            print(f"  Vị trí {i+1}/{key_len}: shift = {shift:2d} → '{ALPHABET[shift]}'")

        key = "".join(ALPHABET[s] for s in shifts)
        plain = decrypt_vigenere(ciphertext, key)

        chi = _chi_square_text(plain)
        status = "✓ BEST" if chi < best_score else ""
        print(f"  → Key: '{key}' | Chi-square: {chi:.2f} {status}")

        if chi < best_score:
            best_score = chi
            best_key = key
            best_plain = plain

    if best_key is not None:
        original_key = best_key
        best_key = _reduce_repeating_key(best_key)
        if best_key != original_key:
            print(f"\n✓ Phát hiện key lặp lại: '{original_key}' → '{best_key}'")
        best_plain = decrypt_vigenere(ciphertext, best_key)

    print("-" * 60)
    print(f"KẾT QUẢ TỐT NHẤT:")
    print(f"  Key tìm được: '{best_key}'")
    print(f"  Chi-square score: {best_score:.2f}")
    print(f"  Plaintext preview: {best_plain[:100]}...")
    print("=" * 60 + "\n")

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
    return _break_vigenere_internal(ciphertext, max_key_len=30, top_k=10)


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
