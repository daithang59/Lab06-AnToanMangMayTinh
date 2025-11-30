# crypto/substitution.py
"""
Task 2 - Monoalphabetic substitution solver
(quadgram + word-bonus, random-restart hill-climb, no external libs)

- Ngôn ngữ: quadgram statistics từ english_quadgrams.txt
- Bonus: dựa trên wordlist.txt (tỉ lệ từ tiếng Anh hợp lệ)
- Tối ưu: simple hill-climbing + random restart

Public API cho Flask:
    from crypto.substitution import break_substitution
    score, mapping_str, plaintext = break_substitution(ciphertext)

CLI cho đúng format đề:
    python -m crypto.substitution -i data/ciphertext.txt -o output_task2.txt
"""

import os
import re
import string
import random
from math import log

ALPHABET = string.ascii_lowercase

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
QUADGRAM_PATH = os.path.join(BASE_DIR, "data", "english_quadgrams.txt")
WORDLIST_PATH = os.path.join(BASE_DIR, "data", "wordlist.txt")

# ----------------------------- global cache ----------------------------- #

_QUAD_LOG = None  # dict[quadgram] -> log P(g)
_QUAD_DEFAULT = None  # default log-prob cho quadgram hiếm
_WORDSET = None  # set các từ trong wordlist


# ========================= 1. Quadgram model ============================ #


def _load_quadgrams():
    """
    Load english_quadgrams.txt:
        mỗi dòng: "ABCD count"
    Tính log-probability với smoothing nhẹ:
        log P(g) = log( (count + 1) / (total + V) ), V = số quadgram khác nhau.
    """
    global _QUAD_LOG, _QUAD_DEFAULT
    if _QUAD_LOG is not None:
        return

    quad_counts = {}
    total = 0

    try:
        with open(QUADGRAM_PATH, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue
                g, c = parts[0], parts[1]
                g = g.lower()
                if len(g) != 4 or not all(ch in ALPHABET for ch in g):
                    continue
                try:
                    cnt = int(c)
                except ValueError:
                    continue
                quad_counts[g] = quad_counts.get(g, 0) + cnt
                total += cnt
    except FileNotFoundError:
        # fallback uniform nếu thiếu file
        _QUAD_LOG = {}
        _QUAD_DEFAULT = log(1.0 / (26**4))
        return

    if total == 0:
        _QUAD_LOG = {}
        _QUAD_DEFAULT = log(1.0 / (26**4))
        return

    V = len(quad_counts)
    QUAD_LOG = {}
    for g, cnt in quad_counts.items():
        QUAD_LOG[g] = log((cnt + 1) / (total + V))

    QUAD_DEFAULT = log(1 / (total + V))

    _QUAD_LOG = QUAD_LOG
    _QUAD_DEFAULT = QUAD_DEFAULT


def _quad_score(text: str) -> float:
    """
    Score plaintext bằng quadgram log-prob.
    Chỉ dùng chữ cái a-z, bỏ hết ký tự khác.
    """
    _load_quadgrams()
    global _QUAD_LOG, _QUAD_DEFAULT

    letters = [c for c in text.lower() if c in ALPHABET]
    if len(letters) < 4:
        return float("-inf")

    s = "".join(letters)
    score = 0.0
    for i in range(len(s) - 3):
        g = s[i : i + 4]
        score += _QUAD_LOG.get(g, _QUAD_DEFAULT)
    return score


# ======================== 2. Wordlist bonus ============================= #


def _load_wordlist():
    """
    Load wordlist.txt thành set các từ tiếng Anh (>=3 ký tự, alphabet).
    """
    global _WORDSET
    if _WORDSET is not None:
        return _WORDSET

    wordset = set()
    try:
        with open(WORDLIST_PATH, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                w = line.strip().lower()
                if len(w) >= 3 and w.isalpha():
                    wordset.add(w)
    except FileNotFoundError:
        wordset = set()

    _WORDSET = wordset
    return wordset


def _word_bonus(text: str) -> float:
    """
    Bonus dựa trên wordlist:
    - Tách word bằng regex [a-zA-Z]{3,}
    - Tính tỉ lệ từ nằm trong wordlist
    - Nhân với hệ số nhỏ để tránh lấn át quadgram
    """
    wordset = _load_wordlist()
    if not wordset:
        return 0.0

    words = re.findall(r"[a-zA-Z]{3,}", text)
    if not words:
        return 0.0

    words = [w.lower() for w in words]
    matched = sum(1 for w in words if w in wordset)
    ratio = matched / len(words)  # 0..1

    # Length factor: văn bản càng dài bonus càng đáng tin
    length_factor = min(len(text) / 4000.0, 2.0)

    # Hệ số bonus nhỏ để quadgram vẫn là chính
    return 35.0 * ratio * length_factor


def _language_score(text: str) -> float:
    """
    Score tổng hợp:
        quadgram log-prob + word-bonus.
    """
    return _quad_score(text) + _word_bonus(text)


# ===================== 3. Key & decrypt utilities ======================= #


def _apply_key(ciphertext: str, key: str) -> str:
    """
    key: chuỗi 26 chữ cái, key[i] = plaintext cho cipher chr(ord('a') + i)
    """
    res = []
    for ch in ciphertext:
        if ch.isalpha():
            lower = ch.lower()
            idx = ord(lower) - ord("a")
            if 0 <= idx < 26:
                p = key[idx]
            else:
                p = lower
            res.append(p.upper() if ch.isupper() else p)
        else:
            res.append(ch)
    return "".join(res)


def _random_key() -> str:
    lst = list(ALPHABET)
    random.shuffle(lst)
    return "".join(lst)


def _swap_positions(key: str, i: int, j: int) -> str:
    """Hoán đổi 2 vị trí trong key (vị trí = cipher letter)."""
    if i == j:
        return key
    lst = list(key)
    lst[i], lst[j] = lst[j], lst[i]
    return "".join(lst)


# ====================== 4. Simple hill-climbing ========================= #


def _hill_climb(cipher_sample: str, max_plateau_moves: int = 1000) -> tuple[float, str]:
    """
    Hill-climbing đơn giản:
    - Bắt đầu với key random.
    - Lặp:
        + Thử TẤT CẢ cặp (i, j) 0 <= i < j < 26.
        + Nếu swap nào cho score tốt hơn -> nhận "first better" và restart loop.
        + Nếu không swap nào tốt hơn -> local optimum -> dừng.
    """
    key = _random_key()
    plaintext = _apply_key(cipher_sample, key)
    best_score = _language_score(plaintext)
    best_key = key

    plateau = 0
    improved = True
    while improved and plateau < max_plateau_moves:
        improved = False
        for i in range(25):
            for j in range(i + 1, 26):
                cand_key = _swap_positions(best_key, i, j)
                cand_plain = _apply_key(cipher_sample, cand_key)
                cand_score = _language_score(cand_plain)
                if cand_score > best_score:
                    best_score = cand_score
                    best_key = cand_key
                    improved = True
                    plateau = 0
                    break
            if improved:
                break
        if not improved:
            plateau += 1

    return best_score, best_key


def _break_with_hillclimb(
    ciphertext: str, rounds: int = 40, sample_letters: int = 6000
):
    """
    Random-restart hill-climbing:
    - ciphertext có thể rất dài; dùng prefix gồm sample_letters chữ cái.
    - Chạy 'rounds' lần hill-climb độc lập, giữ best score toàn cục.
    """
    letters = [c for c in ciphertext if c.isalpha()]
    if not letters:
        return 0.0, ALPHABET

    if len(letters) > sample_letters:
        sample = "".join(letters[:sample_letters])
    else:
        sample = "".join(letters)

    global_best_score = float("-inf")
    global_best_key = ALPHABET

    for _ in range(rounds):
        score, key = _hill_climb(sample)
        if score > global_best_score:
            global_best_score = score
            global_best_key = key

    return global_best_score, global_best_key


# ============================= 5. Public API ============================ #


def break_substitution(ciphertext: str):
    """
    Hàm dùng trong Flask.

    Trả về:
        score (float),
        mapping_str: "cipher: abcdef... | plain : <key>",
        plaintext: ciphertext đã giải với key tốt nhất.
    """
    random.seed()

    if not ciphertext:
        mapping_str = "cipher: " + ALPHABET + " | plain : " + ALPHABET
        return 0.0, mapping_str, ""

    score, key = _break_with_hillclimb(ciphertext, rounds=40, sample_letters=6000)

    plaintext = _apply_key(ciphertext, key)
    cipher_line = "cipher: " + ALPHABET
    plain_line = "plain : " + key
    mapping_str = cipher_line + " | " + plain_line

    return score, mapping_str, plaintext


# ============================== 6. CLI mode ============================= #


def _run_cli():
    """
    Chạy từ command line đúng format đề:
        dòng 1: score
        dòng 2: mapping
        dòng 3+: plaintext
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Task 2 - Substitution cipher breaker (quadgram + word-bonus)"
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Đường dẫn file ciphertext"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Đường dẫn file plaintext output"
    )
    parser.add_argument(
        "--rounds", type=int, default=40, help="Số round hill-climb (mặc định 40)"
    )
    parser.add_argument(
        "--sample", type=int, default=6000, help="Số chữ cái dùng cho scoring sample"
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
        ciphertext = f.read()

    random.seed()
    score, key = _break_with_hillclimb(
        ciphertext, rounds=args.rounds, sample_letters=args.sample
    )
    plaintext = _apply_key(ciphertext, key)

    cipher_line = "cipher: " + ALPHABET
    plain_line = "plain : " + key
    mapping_str = cipher_line + " | " + plain_line

    with open(args.output, "w", encoding="utf-8", errors="ignore") as out:
        out.write(str(score) + "\n")
        out.write(mapping_str + "\n")
        out.write(plaintext)

    print(f"[+] Done. Score = {score:.2f}")
    print(f"[+] {mapping_str}")


if __name__ == "__main__":
    _run_cli()
