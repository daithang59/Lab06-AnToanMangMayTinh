# crypto/substitution.py
"""
Task 2 - Monoalphabetic substitution solver
(quadgram + word-bonus, random-restart hill-climb, no external libs)

- Ngôn ngữ: quadgram statistics từ english_quadgrams.txt
- Bonus: dựa trên wordlist.txt (tỉ lệ từ tiếng Anh hợp lệ)
- Tối ưu: simple hill-climbing + random restart

"""

import os
import re
import string
import random
from math import log

ALPHABET = string.ascii_lowercase

# Pre-compile regex for better performance
WORD_PATTERN = re.compile(r"[a-zA-Z]{3,}")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MONOGRAM_PATH = os.path.join(BASE_DIR, "data", "english_monograms.txt")
BIGRAM_PATH = os.path.join(BASE_DIR, "data", "english_bigrams.txt")
TRIGRAM_PATH = os.path.join(BASE_DIR, "data", "english_trigrams.txt")
QUADGRAM_PATH = os.path.join(BASE_DIR, "data", "english_quadgrams.txt")
WORDLIST_PATH = os.path.join(BASE_DIR, "data", "wordlist.txt")

# ----------------------------- global cache ----------------------------- #

_MONO_FREQ = None  # dict[letter] -> frequency
_BI_LOG = None  # dict[bigram] -> log P
_BI_DEFAULT = None
_TRI_LOG = None  # dict[trigram] -> log P
_TRI_DEFAULT = None
_QUAD_LOG = None  # dict[quadgram] -> log P(g)
_QUAD_DEFAULT = None  # default log-prob cho quadgram hiếm
_WORDSET = None  # set các từ trong wordlist


# ========================= 1. N-gram models ============================ #


def _load_monograms():
    """
    Load english_monograms.txt để có frequency chính xác hơn cho seed.
    Format: "E 529117365"
    """
    global _MONO_FREQ
    if _MONO_FREQ is not None:
        return

    mono_freq = {}
    total = 0

    try:
        with open(MONOGRAM_PATH, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue
                letter, count = parts[0].lower(), parts[1]
                if len(letter) != 1 or letter not in ALPHABET:
                    continue
                try:
                    cnt = int(count)
                    mono_freq[letter] = cnt
                    total += cnt
                except ValueError:
                    continue
    except FileNotFoundError:
        # Fallback to default English frequency
        _MONO_FREQ = {}
        return

    _MONO_FREQ = mono_freq


def _load_bigrams():
    """
    Load english_bigrams.txt cho bigram scoring.
    Format: "TH 116997844"
    """
    global _BI_LOG, _BI_DEFAULT
    if _BI_LOG is not None:
        return

    bi_counts = {}
    total = 0

    try:
        with open(BIGRAM_PATH, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue
                bigram, count = parts[0].lower(), parts[1]
                if len(bigram) != 2 or not all(c in ALPHABET for c in bigram):
                    continue
                try:
                    cnt = int(count)
                    bi_counts[bigram] = cnt
                    total += cnt
                except ValueError:
                    continue
    except FileNotFoundError:
        _BI_LOG = {}
        _BI_DEFAULT = log(1.0 / (26**2))
        return

    if total == 0:
        _BI_LOG = {}
        _BI_DEFAULT = log(1.0 / (26**2))
        return

    V = len(bi_counts)
    BI_LOG = {}
    for bg, cnt in bi_counts.items():
        BI_LOG[bg] = log((cnt + 1) / (total + V))

    _BI_LOG = BI_LOG
    _BI_DEFAULT = log(1 / (total + V))


def _load_trigrams():
    """
    Load english_trigrams.txt cho trigram scoring.
    Format: "THE 77534223"
    """
    global _TRI_LOG, _TRI_DEFAULT
    if _TRI_LOG is not None:
        return

    tri_counts = {}
    total = 0

    try:
        with open(TRIGRAM_PATH, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue
                trigram, count = parts[0].lower(), parts[1]
                if len(trigram) != 3 or not all(c in ALPHABET for c in trigram):
                    continue
                try:
                    cnt = int(count)
                    tri_counts[trigram] = cnt
                    total += cnt
                except ValueError:
                    continue
    except FileNotFoundError:
        _TRI_LOG = {}
        _TRI_DEFAULT = log(1.0 / (26**3))
        return

    if total == 0:
        _TRI_LOG = {}
        _TRI_DEFAULT = log(1.0 / (26**3))
        return

    V = len(tri_counts)
    TRI_LOG = {}
    for tg, cnt in tri_counts.items():
        TRI_LOG[tg] = log((cnt + 1) / (total + V))

    _TRI_LOG = TRI_LOG
    _TRI_DEFAULT = log(1 / (total + V))


# ========================= Quadgram model (existing) ==================== #


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


# ======================== 2. Wordlist bonus ============================= #


def _load_wordlist():
    """
    Load wordlist.txt thành set các từ tiếng Anh (>=3 ký tự, alphabet).
    Thử load wordlist_enhanced.txt trước, fallback về wordlist.txt
    """
    global _WORDSET
    if _WORDSET is not None:
        return _WORDSET

    wordset = set()

    # Try enhanced wordlist first
    enhanced_path = os.path.join(BASE_DIR, "data", "wordlist_enhanced.txt")
    paths_to_try = [enhanced_path, WORDLIST_PATH]

    for path in paths_to_try:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    w = line.strip().lower()
                    if len(w) >= 3 and w.isalpha():
                        wordset.add(w)
            if wordset:  # If we got words, stop trying
                break
        except FileNotFoundError:
            continue

    _WORDSET = wordset
    return wordset


def _word_bonus(text: str) -> float:
    """
    Bonus dựa trên wordlist - TỐI ƯU CHO ACCURACY:
    - Kiểm tra TẤT CẢ các từ (không sample)
    - Weight cao để ưu tiên plaintext có nhiều từ hợp lệ
    """
    wordset = _load_wordlist()
    if not wordset:
        return 0.0

    words = WORD_PATTERN.findall(text)
    if not words:
        return 0.0

    # Kiểm tra TẤT CẢ từ - không sample
    matched = sum(1 for w in words if w.lower() in wordset)
    ratio = matched / len(words)

    # Weight cao + length factor để ưu tiên accuracy
    length_factor = min(len(text) / 2000.0, 2.0)

    return 150.0 * ratio * length_factor


def _ngram_score(
    text: str, weights: tuple[float, float, float] = (0.10, 0.20, 0.70)
) -> float:
    """
    Combined n-gram scoring với weighted sum:
    - Bigram: weight thấp (pattern cơ bản)
    - Trigram: weight trung bình
    - Quadgram: weight cao nhất (optimal)

    Args:
        text: văn bản cần chấm điểm
        weights: tuple (bigram_weight, trigram_weight, quadgram_weight)
                 Mặc định: (0.10, 0.20, 0.70)

    Returns:
        float: điểm n-gram tổng hợp
    """
    _load_bigrams()
    _load_trigrams()
    _load_quadgrams()

    text_lower = text.lower()
    s = "".join(c for c in text_lower if c in ALPHABET)
    s_len = len(s)

    if s_len < 2:
        return float("-inf")

    score = 0.0
    bi_weight, tri_weight, quad_weight = weights

    # Bigram scoring
    if s_len >= 2 and _BI_LOG:
        bi_score = sum(_BI_LOG.get(s[i : i + 2], _BI_DEFAULT) for i in range(s_len - 1))
        score += bi_weight * bi_score

    # Trigram scoring
    if s_len >= 3 and _TRI_LOG:
        tri_score = sum(
            _TRI_LOG.get(s[i : i + 3], _TRI_DEFAULT) for i in range(s_len - 2)
        )
        score += tri_weight * tri_score

    # Quadgram scoring
    if s_len >= 4 and _QUAD_LOG:
        quad_score = sum(
            _QUAD_LOG.get(s[i : i + 4], _QUAD_DEFAULT) for i in range(s_len - 3)
        )
        score += quad_weight * quad_score

    return score


def _language_score(text: str) -> float:
    """
    Score tổng hợp - TỐI ƯU CHO ACCURACY CAO NHẤT:
        Sử dụng full n-gram suite: bigram + trigram + quadgram + word bonus

    Weight distribution:
        - Bigram: 10% (pattern cơ bản)
        - Trigram: 20% (context ngắn)
        - Quadgram: 60% (context dài - chính)
        - Word bonus: ~10% equivalent (validation từ điển)

    Returns:
        float: điểm tổng hợp (n-gram + word bonus)
    """
    # Sử dụng _ngram_score với weight tùy chỉnh (60% quadgram thay vì 70%)
    ngram_score = _ngram_score(text, weights=(0.10, 0.20, 0.60))

    # Thêm word bonus để tăng accuracy
    word_score = _word_bonus(text)

    return ngram_score + word_score


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


def _frequency_seed(ciphertext: str) -> str:
    """
    Tạo initial key từ frequency analysis (như đề gợi ý).
    Map các ký tự cipher theo tần suất → ký tự tiếng Anh theo tần suất.

    Sử dụng monogram data thực tế thay vì hardcode.
    """
    _load_monograms()
    global _MONO_FREQ

    # Nếu có monogram data, dùng nó; nếu không fallback
    if _MONO_FREQ:
        # Sort theo frequency descending
        english_freq_list = sorted(
            _MONO_FREQ.keys(), key=lambda x: _MONO_FREQ[x], reverse=True
        )
        ENGLISH_FREQ = "".join(english_freq_list)
    else:
        # Fallback to hardcoded
        ENGLISH_FREQ = "etaoinshrdlcumwfgypbvkjxqz"

    # Đếm tần suất trong ciphertext (chỉ chữ cái)
    letter_counts = {}
    for ch in ciphertext.lower():
        if ch in ALPHABET:
            letter_counts[ch] = letter_counts.get(ch, 0) + 1

    if not letter_counts:
        return ALPHABET

    # Sort theo tần suất descending
    cipher_freq = sorted(
        letter_counts.keys(), key=lambda x: letter_counts.get(x, 0), reverse=True
    )

    # Padding các chữ chưa xuất hiện
    for ch in ALPHABET:
        if ch not in cipher_freq:
            cipher_freq.append(ch)

    # Map: cipher[0] (most frequent) → 'e', cipher[1] → 't', ...
    key = list(ALPHABET)  # default identity mapping
    for i, cipher_ch in enumerate(cipher_freq[:26]):
        idx = ord(cipher_ch) - ord("a")
        if i < 26:
            key[idx] = ENGLISH_FREQ[i]

    return "".join(key)


def _swap_positions(key: str, i: int, j: int) -> str:
    """Hoán đổi 2 vị trí trong key (vị trí = cipher letter)."""
    if i == j:
        return key
    lst = list(key)
    lst[i], lst[j] = lst[j], lst[i]
    return "".join(lst)


# ====================== 4. Simple hill-climbing ========================= #


def _hill_climb(
    cipher_sample: str,
    use_freq_seed: bool = False,
    max_iterations: int = 2000,
    use_annealing: bool = False,
) -> tuple[float, str]:
    """
    Hill-climbing tối ưu:
    - Bắt đầu với key frequency-based HOẶC random.
    - Lặp:
        + Thử TẤT CẢ cặp (i, j) 0 <= i < j < 26.
        + Nếu swap nào cho score tốt hơn -> nhận "first better" và restart loop.
        + Nếu không swap nào tốt hơn -> local optimum -> dừng.
    - Optimized: cache plaintext, chỉ update phần thay đổi

    Args:
        cipher_sample: Text mẫu để scoring
        use_freq_seed: Nếu True, dùng frequency analysis làm seed; False = random
        max_iterations: Số iteration tối đa (giảm từ 3000 xuống 2000 cho web)
        use_annealing: Nếu True, dùng simulated annealing để tránh local optimum
    """
    if use_freq_seed:
        key = _frequency_seed(cipher_sample)
    else:
        key = _random_key()

    plaintext = _apply_key(cipher_sample, key)
    best_score = _language_score(plaintext)
    best_key = key
    current_score = best_score
    current_key = key

    # Simulated annealing với nhiệt độ cao hơn cho accuracy
    temperature = 30.0 if use_annealing else 0.0
    cooling_rate = 0.995

    iterations = 0
    improved = True
    while improved and iterations < max_iterations:
        improved = False
        for i in range(25):
            for j in range(i + 1, 26):
                cand_key = _swap_positions(current_key, i, j)
                cand_plain = _apply_key(cipher_sample, cand_key)
                cand_score = _language_score(cand_plain)

                # Standard hill-climbing: always accept better
                if cand_score > current_score:
                    current_score = cand_score
                    current_key = cand_key
                    plaintext = cand_plain
                    improved = True
                    iterations = 0

                    # Track global best
                    if current_score > best_score:
                        best_score = current_score
                        best_key = current_key
                    break

                # Simulated annealing: sometimes accept worse with probability
                elif use_annealing and temperature > 0.1:
                    import math

                    delta = cand_score - current_score
                    acceptance_prob = math.exp(delta / temperature)
                    if random.random() < acceptance_prob:
                        current_score = cand_score
                        current_key = cand_key
                        improved = True
                        break

            if improved:
                break

        if not improved:
            iterations += 1

        # Cool down temperature
        if use_annealing:
            temperature *= cooling_rate

    return best_score, best_key


def _break_with_hillclimb(
    ciphertext: str,
    rounds: int = 80,
    sample_letters: int = 8000,
    consolidate: int = 6,
):
    """
    Random-restart hill-climbing - TỐI ƯU CHO ACCURACY:
    - Nhiều rounds để tăng cơ hội tìm global optimum
    - Sample size lớn để phân tích chính xác
    - Consolidate cao để xác nhận kết quả
    - Sử dụng cả frequency seed và simulated annealing
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
    local_maximum_hits = 0
    no_improvement_count = 0

    for round_num in range(rounds):
        # Round đầu: frequency seed (baseline tốt nhất)
        # Mỗi 4 round: dùng annealing để escape local optimum (tần suất cao)
        # Các round khác: random restart
        use_freq = round_num == 0
        use_anneal = round_num > 0 and round_num % 4 == 0

        score, key = _hill_climb(
            sample, use_freq_seed=use_freq, use_annealing=use_anneal
        )

        if score > global_best_score + 0.3:  # Chấp nhận cải thiện nhỏ hơn
            global_best_score = score
            global_best_key = key
            local_maximum_hits = 1
            no_improvement_count = 0
        elif abs(score - global_best_score) < 0.3:  # Tolerance nhỏ hơn
            local_maximum_hits += 1
            if local_maximum_hits >= consolidate:
                # Đã confirm nhiều lần - đây là kết quả tốt nhất
                break
        else:
            no_improvement_count += 1

        # Kiên nhẫn hơn - chỉ stop nếu thực sự stuck
        if no_improvement_count > 20:
            break

    return global_best_score, global_best_key


# ============================= 5. Public API ============================ #


def break_substitution(ciphertext: str, rounds: int = 80, consolidate: int = 6):
    """
    Hàm dùng trong Flask - TỐI ƯU CHO ĐỘ CHÍNH XÁC CAO NHẤT.

    Trả về:
        score (float),
        mapping_str: "cipher: abcdef... | plain : <key>",
        plaintext: ciphertext đã giải với key tốt nhất.

    Args:
        ciphertext: văn bản mã hóa cần giải
        rounds: số vòng hill-climb tối đa (80 - cao để đảm bảo accuracy)
        consolidate: số lần cần đạt cùng kết quả để xác nhận (6 - chắc chắn)
    """
    random.seed()

    if not ciphertext:
        mapping_str = "cipher: " + ALPHABET + " | plain : " + ALPHABET
        return 0.0, mapping_str, ""

    # Sử dụng sample size lớn để đảm bảo accuracy cao
    letters = [c for c in ciphertext if c.isalpha()]
    # Ưu tiên accuracy hơn speed
    if len(letters) > 8000:
        sample_size = 6000  # File rất lớn -> vẫn sample nhiều
    elif len(letters) > 4000:
        sample_size = 7000  # File lớn -> sample rất nhiều
    else:
        sample_size = len(letters)  # File nhỏ -> dùng hết

    score, key = _break_with_hillclimb(
        ciphertext, rounds=rounds, sample_letters=sample_size, consolidate=consolidate
    )

    plaintext = _apply_key(ciphertext, key)

    # Format mapping rõ ràng hơn (theo đề bài)
    cipher_line = "CIPHER: " + ALPHABET.upper()
    plain_line = "PLAIN : " + key.upper()
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
        "--rounds", type=int, default=150, help="Số round hill-climb (mặc định 150)"
    )
    parser.add_argument(
        "--sample", type=int, default=10000, help="Số chữ cái dùng cho scoring sample"
    )
    parser.add_argument(
        "--consolidate",
        type=int,
        default=8,
        help="Số lần cần đạt cùng kết quả (mặc định 8)",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
        ciphertext = f.read()

    random.seed()
    score, key = _break_with_hillclimb(
        ciphertext,
        rounds=args.rounds,
        sample_letters=args.sample,
        consolidate=args.consolidate,
    )
    plaintext = _apply_key(ciphertext, key)

    cipher_line = "cipher: " + ALPHABET.upper()
    plain_line = "plain : " + key.upper()

    with open(args.output, "w", encoding="utf-8", errors="ignore") as out:
        # Dòng 1: Score/log-likelihood (rõ ràng như đề yêu cầu)
        out.write(f"Score / Log-likelihood: {score:.2f}\n")
        # Dòng 2: Mapping
        out.write(cipher_line + "\n")
        out.write(plain_line + "\n")
        # Dòng 3+: Plaintext
        out.write(plaintext)

    print(f"[+] Done. Score / Log-likelihood = {score:.2f}")
    print(f"[+] Mapping:")
    print(f"    {cipher_line}")
    print(f"    {plain_line}")


if __name__ == "__main__":
    _run_cli()
