# crypto/aes_core.py
"""
AES core implementation (128/192/256-bit keys)
---------------------------------------------
- key_expansion(key) -> round_keys (list of Nr+1 round keys, mỗi key 16 bytes)
- aes_encrypt_block(block16, round_keys)
- aes_decrypt_block(block16, round_keys)

Hỗ trợ:
- AES-128: key 16 bytes  -> Nk=4,  Nr=10
- AES-192: key 24 bytes  -> Nk=6,  Nr=12
- AES-256: key 32 bytes  -> Nk=8,  Nr=14

Block size luôn là 16 bytes (128 bit) theo chuẩn AES.
"""

S_BOX = [
    0x63,
    0x7C,
    0x77,
    0x7B,
    0xF2,
    0x6B,
    0x6F,
    0xC5,
    0x30,
    0x01,
    0x67,
    0x2B,
    0xFE,
    0xD7,
    0xAB,
    0x76,
    0xCA,
    0x82,
    0xC9,
    0x7D,
    0xFA,
    0x59,
    0x47,
    0xF0,
    0xAD,
    0xD4,
    0xA2,
    0xAF,
    0x9C,
    0xA4,
    0x72,
    0xC0,
    0xB7,
    0xFD,
    0x93,
    0x26,
    0x36,
    0x3F,
    0xF7,
    0xCC,
    0x34,
    0xA5,
    0xE5,
    0xF1,
    0x71,
    0xD8,
    0x31,
    0x15,
    0x04,
    0xC7,
    0x23,
    0xC3,
    0x18,
    0x96,
    0x05,
    0x9A,
    0x07,
    0x12,
    0x80,
    0xE2,
    0xEB,
    0x27,
    0xB2,
    0x75,
    0x09,
    0x83,
    0x2C,
    0x1A,
    0x1B,
    0x6E,
    0x5A,
    0xA0,
    0x52,
    0x3B,
    0xD6,
    0xB3,
    0x29,
    0xE3,
    0x2F,
    0x84,
    0x53,
    0xD1,
    0x00,
    0xED,
    0x20,
    0xFC,
    0xB1,
    0x5B,
    0x6A,
    0xCB,
    0xBE,
    0x39,
    0x4A,
    0x4C,
    0x58,
    0xCF,
    0xD0,
    0xEF,
    0xAA,
    0xFB,
    0x43,
    0x4D,
    0x33,
    0x85,
    0x45,
    0xF9,
    0x02,
    0x7F,
    0x50,
    0x3C,
    0x9F,
    0xA8,
    0x51,
    0xA3,
    0x40,
    0x8F,
    0x92,
    0x9D,
    0x38,
    0xF5,
    0xBC,
    0xB6,
    0xDA,
    0x21,
    0x10,
    0xFF,
    0xF3,
    0xD2,
    0xCD,
    0x0C,
    0x13,
    0xEC,
    0x5F,
    0x97,
    0x44,
    0x17,
    0xC4,
    0xA7,
    0x7E,
    0x3D,
    0x64,
    0x5D,
    0x19,
    0x73,
    0x60,
    0x81,
    0x4F,
    0xDC,
    0x22,
    0x2A,
    0x90,
    0x88,
    0x46,
    0xEE,
    0xB8,
    0x14,
    0xDE,
    0x5E,
    0x0B,
    0xDB,
    0xE0,
    0x32,
    0x3A,
    0x0A,
    0x49,
    0x06,
    0x24,
    0x5C,
    0xC2,
    0xD3,
    0xAC,
    0x62,
    0x91,
    0x95,
    0xE4,
    0x79,
    0xE7,
    0xC8,
    0x37,
    0x6D,
    0x8D,
    0xD5,
    0x4E,
    0xA9,
    0x6C,
    0x56,
    0xF4,
    0xEA,
    0x65,
    0x7A,
    0xAE,
    0x08,
    0xBA,
    0x78,
    0x25,
    0x2E,
    0x1C,
    0xA6,
    0xB4,
    0xC6,
    0xE8,
    0xDD,
    0x74,
    0x1F,
    0x4B,
    0xBD,
    0x8B,
    0x8A,
    0x70,
    0x3E,
    0xB5,
    0x66,
    0x48,
    0x03,
    0xF6,
    0x0E,
    0x61,
    0x35,
    0x57,
    0xB9,
    0x86,
    0xC1,
    0x1D,
    0x9E,
    0xE1,
    0xF8,
    0x98,
    0x11,
    0x69,
    0xD9,
    0x8E,
    0x94,
    0x9B,
    0x1E,
    0x87,
    0xE9,
    0xCE,
    0x55,
    0x28,
    0xDF,
    0x8C,
    0xA1,
    0x89,
    0x0D,
    0xBF,
    0xE6,
    0x42,
    0x68,
    0x41,
    0x99,
    0x2D,
    0x0F,
    0xB0,
    0x54,
    0xBB,
    0x16,
]

INV_S_BOX = [0] * 256
for i, v in enumerate(S_BOX):
    INV_S_BOX[v] = i

# Rcon cho key expansion (đủ dùng cho AES-256)
RCON = [
    0x00,
    0x01,
    0x02,
    0x04,
    0x08,
    0x10,
    0x20,
    0x40,
    0x80,
    0x1B,
    0x36,
    0x6C,
    0xD8,
    0xAB,
    0x4D,
    0x9A,
]


def _sub_word(word: int) -> int:
    return (
        (S_BOX[(word >> 24) & 0xFF] << 24)
        | (S_BOX[(word >> 16) & 0xFF] << 16)
        | (S_BOX[(word >> 8) & 0xFF] << 8)
        | (S_BOX[word & 0xFF])
    )


def _rot_word(word: int) -> int:
    return ((word << 8) & 0xFFFFFFFF) | (word >> 24)


def key_expansion(key: bytes):
    """
    Hỗ trợ key:
        - 16 bytes: AES-128 (Nk=4,  Nr=10)
        - 24 bytes: AES-192 (Nk=6,  Nr=12)
        - 32 bytes: AES-256 (Nk=8,  Nr=14)
    Trả về:
        round_keys: list[bytes] gồm Nr+1 round key, mỗi key 16 bytes.
    """
    key_len = len(key)
    if key_len not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes long")

    Nk = key_len // 4  # 4, 6, 8
    Nb = 4
    Nr = Nk + 6  # 10, 12, 14

    w = [0] * (Nb * (Nr + 1))

    # copy key vào w[0..Nk-1]
    for i in range(Nk):
        w[i] = (
            (key[4 * i] << 24)
            | (key[4 * i + 1] << 16)
            | (key[4 * i + 2] << 8)
            | key[4 * i + 3]
        )

    # mở rộng key
    for i in range(Nk, Nb * (Nr + 1)):
        temp = w[i - 1]
        if i % Nk == 0:
            temp = _sub_word(_rot_word(temp)) ^ (RCON[i // Nk] << 24)
        elif Nk > 6 and i % Nk == 4:
            # trường hợp AES-256
            temp = _sub_word(temp)
        w[i] = w[i - Nk] ^ temp

    # gom lại thành round_keys (mỗi key 16 bytes)
    round_keys = []
    for r in range(Nr + 1):
        key_bytes = bytearray(16)
        for c in range(4):
            word = w[r * 4 + c]
            key_bytes[4 * c] = (word >> 24) & 0xFF
            key_bytes[4 * c + 1] = (word >> 16) & 0xFF
            key_bytes[4 * c + 2] = (word >> 8) & 0xFF
            key_bytes[4 * c + 3] = word & 0xFF
        round_keys.append(bytes(key_bytes))
    return round_keys


def _add_round_key(state, round_key):
    for i in range(16):
        state[i] ^= round_key[i]


def _sub_bytes(state):
    for i in range(16):
        state[i] = S_BOX[state[i]]


def _inv_sub_bytes(state):
    for i in range(16):
        state[i] = INV_S_BOX[state[i]]


def _shift_rows(state):
    s = list(state)
    state[0] = s[0]
    state[1] = s[5]
    state[2] = s[10]
    state[3] = s[15]

    state[4] = s[4]
    state[5] = s[9]
    state[6] = s[14]
    state[7] = s[3]

    state[8] = s[8]
    state[9] = s[13]
    state[10] = s[2]
    state[11] = s[7]

    state[12] = s[12]
    state[13] = s[1]
    state[14] = s[6]
    state[15] = s[11]


def _inv_shift_rows(state):
    s = list(state)
    state[0] = s[0]
    state[1] = s[13]
    state[2] = s[10]
    state[3] = s[7]

    state[4] = s[4]
    state[5] = s[1]
    state[6] = s[14]
    state[7] = s[11]

    state[8] = s[8]
    state[9] = s[5]
    state[10] = s[2]
    state[11] = s[15]

    state[12] = s[12]
    state[13] = s[9]
    state[14] = s[6]
    state[15] = s[3]


def _xtime(a):
    return ((a << 1) & 0xFF) ^ (0x1B if a & 0x80 else 0x00)


def _mul(a, b):
    res = 0
    while b:
        if b & 1:
            res ^= a
        a = _xtime(a)
        b >>= 1
    return res


def _mix_columns(state):
    for c in range(4):
        i = 4 * c
        a0, a1, a2, a3 = state[i], state[i + 1], state[i + 2], state[i + 3]
        state[i] = _mul(a0, 2) ^ _mul(a1, 3) ^ a2 ^ a3
        state[i + 1] = a0 ^ _mul(a1, 2) ^ _mul(a2, 3) ^ a3
        state[i + 2] = a0 ^ a1 ^ _mul(a2, 2) ^ _mul(a3, 3)
        state[i + 3] = _mul(a0, 3) ^ a1 ^ a2 ^ _mul(a3, 2)


def _inv_mix_columns(state):
    for c in range(4):
        i = 4 * c
        a0, a1, a2, a3 = state[i], state[i + 1], state[i + 2], state[i + 3]
        state[i] = _mul(a0, 14) ^ _mul(a1, 11) ^ _mul(a2, 13) ^ _mul(a3, 9)
        state[i + 1] = _mul(a0, 9) ^ _mul(a1, 14) ^ _mul(a2, 11) ^ _mul(a3, 13)
        state[i + 2] = _mul(a0, 13) ^ _mul(a1, 9) ^ _mul(a2, 14) ^ _mul(a3, 11)
        state[i + 3] = _mul(a0, 11) ^ _mul(a1, 13) ^ _mul(a2, 9) ^ _mul(a3, 14)


def aes_encrypt_block(block16: bytes, round_keys) -> bytes:
    if len(block16) != 16:
        raise ValueError("AES block must be 16 bytes")

    state = bytearray(block16)
    Nr = len(round_keys) - 1

    _add_round_key(state, round_keys[0])

    for r in range(1, Nr):
        _sub_bytes(state)
        _shift_rows(state)
        _mix_columns(state)
        _add_round_key(state, round_keys[r])

    _sub_bytes(state)
    _shift_rows(state)
    _add_round_key(state, round_keys[Nr])

    return bytes(state)


def aes_decrypt_block(block16: bytes, round_keys) -> bytes:
    if len(block16) != 16:
        raise ValueError("AES block must be 16 bytes")

    state = bytearray(block16)
    Nr = len(round_keys) - 1

    _add_round_key(state, round_keys[Nr])
    _inv_shift_rows(state)
    _inv_sub_bytes(state)

    for r in range(Nr - 1, 0, -1):
        _add_round_key(state, round_keys[r])
        _inv_mix_columns(state)
        _inv_shift_rows(state)
        _inv_sub_bytes(state)

    _add_round_key(state, round_keys[0])
    return bytes(state)
