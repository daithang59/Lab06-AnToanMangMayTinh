"""
Vigenère Cipher Breaker (Key unknown)
-------------------------------------
- Dùng Index of Coincidence (IC) để đoán độ dài khóa.
- Mỗi "cột" là một Caesar -> phá bằng chi-square.
"""

import string
from math import gcd

ALPHABET = string.ascii_uppercase
ALPHABET_LEN = 26


def _only_letters(text: str) -> str:
    return ''.join(c for c in text.upper() if c.isalpha())


def _index_of_coincidence(seq: str) -> float:
    """
    IC = sum(f_i (f_i - 1)) / (N (N - 1))
    """
    N = len(seq)
    if N <= 1:
        return 0.0
    counts = [0] * ALPHABET_LEN
    for c in seq:
        if c in ALPHABET:
            counts[ord(c) - ord('A')] += 1
    num = sum(f * (f - 1) for f in counts)
    den = N * (N - 1)
    return num / den if den else 0.0


def _guess_key_length(ciphertext: str, max_len: int = 20) -> int:
    """
    Đoán độ dài khóa bằng IC: thử L=1..max_len, chọn L có average IC gần 0.065 nhất.
    """
    filtered = _only_letters(ciphertext)
    if not filtered:
        return 1

    best_L = 1
    best_diff = 1e9
    target_IC = 0.065

    for L in range(1, max_len + 1):
        columns = [''] * L
        for i, c in enumerate(filtered):
            columns[i % L] += c
        avg_ic = sum(_index_of_coincidence(col) for col in columns) / L
        diff = abs(avg_ic - target_IC)
        if diff < best_diff:
            best_diff = diff
            best_L = L

    return best_L


# Chi-square cho 1 chuỗi (giống Task 1, nhưng gọn)
ENGLISH_FREQ = [
    8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02,
    6.09, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75,
    7.51, 1.93, 0.10, 5.99, 6.33, 9.06,
    2.76, 0.98, 2.36, 0.15, 1.97, 0.07
]


def _chi_square(text: str) -> float:
    counts = [0] * ALPHABET_LEN
    total = 0
    for c in text:
        if c in ALPHABET:
            idx = ord(c) - ord('A')
            counts[idx] += 1
            total += 1
    if total == 0:
        return 1e9
    chi = 0.0
    for i in range(ALPHABET_LEN):
        observed = counts[i]
        expected = ENGLISH_FREQ[i] * total / 100
        if expected > 0:
            chi += (observed - expected) ** 2 / expected
    return chi


def _best_shift_for_column(col: str) -> int:
    """
    Tìm shift (0-25) tốt nhất cho 1 cột (coi như Caesar).
    """
    best_k = 0
    best_chi = 1e9
    for k in range(26):
        decrypted = []
        for c in col:
            if c in ALPHABET:
                decrypted.append(chr((ord(c) - ord('A') - k) % 26 + ord('A')))
        chi = _chi_square(''.join(decrypted))
        if chi < best_chi:
            best_chi = chi
            best_k = k
    return best_k


def _decrypt_vigenere(ciphertext: str, key: str) -> str:
    """
    Giải mã, giữ nguyên non-letter, nhưng key chỉ áp dụng lên chữ cái.
    """
    res = []
    key = key.upper()
    key_len = len(key)
    j = 0
    for c in ciphertext:
        if c.isalpha():
            base = 'A' if c.isupper() else 'a'
            k = ord(key[j % key_len]) - ord('A')
            p = chr((ord(c) - ord(base) - k) % 26 + ord(base))
            res.append(p)
            j += 1
        else:
            res.append(c)
    return ''.join(res)


def break_vigenere(ciphertext: str):
    """
    API chính cho Flask: trả về (key, plaintext)
    """
    filtered = _only_letters(ciphertext)
    if not filtered:
        return "", ciphertext

    key_len = _guess_key_length(ciphertext)
    # Tách cột
    cols = [''] * key_len
    for i, c in enumerate(filtered):
        cols[i % key_len] += c

    # Tìm shift cho từng cột
    shifts = [_best_shift_for_column(col) for col in cols]
    key = ''.join(chr(ord('A') + k) for k in shifts)

    plaintext = _decrypt_vigenere(ciphertext, key)
    return key, plaintext

