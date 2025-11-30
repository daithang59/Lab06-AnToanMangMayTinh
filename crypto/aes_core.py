# crypto/aes_core.py
"""
AES-128 core implementation
---------------------------
- key_expansion(key16) -> round_keys (list of 11 keys, mỗi key 16 bytes)
- aes_encrypt_block(block16, round_keys)
- aes_decrypt_block(block16, round_keys)
"""

# S-box, inverse S-box, Rcon
S_BOX = [
    # 0     1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

INV_S_BOX = [0] * 256
for i, v in enumerate(S_BOX):
    INV_S_BOX[v] = i

RCON = [
    0x00,
    0x01,0x02,0x04,0x08,
    0x10,0x20,0x40,0x80,
    0x1B,0x36
]


def _sub_word(word: int) -> int:
    return (S_BOX[(word >> 24) & 0xFF] << 24) | \
           (S_BOX[(word >> 16) & 0xFF] << 16) | \
           (S_BOX[(word >> 8) & 0xFF] << 8) | \
           (S_BOX[word & 0xFF])


def _rot_word(word: int) -> int:
    return ((word << 8) & 0xFFFFFFFF) | (word >> 24)


def key_expansion(key: bytes):
    """
    key: 16 bytes
    return: list of round keys, mỗi round key là 16 bytes (11 keys cho AES-128)
    """
    if len(key) != 16:
        raise ValueError("AES-128 key must be 16 bytes")

    Nk = 4
    Nb = 4
    Nr = 10

    # w[i] là 32-bit
    w = [0] * (Nb * (Nr + 1))

    # key ban đầu
    for i in range(Nk):
        w[i] = (key[4*i] << 24) | (key[4*i+1] << 16) | (key[4*i+2] << 8) | key[4*i+3]

    for i in range(Nk, Nb * (Nr + 1)):
        temp = w[i-1]
        if i % Nk == 0:
            temp = _sub_word(_rot_word(temp)) ^ (RCON[i // Nk] << 24)
        w[i] = w[i-Nk] ^ temp

    # convert w[] -> round keys (list of 16-byte)
    round_keys = []
    for r in range(Nr + 1):
        key_bytes = bytearray(16)
        for c in range(4):
            word = w[r*4 + c]
            key_bytes[4*c]   = (word >> 24) & 0xFF
            key_bytes[4*c+1] = (word >> 16) & 0xFF
            key_bytes[4*c+2] = (word >> 8) & 0xFF
            key_bytes[4*c+3] = word & 0xFF
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
    # state là 16 bytes, column-major
    # row1 shift left 1, row2 shift left 2, row3 shift left 3
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
    # GF(2^8) multiplication
    res = 0
    while b:
        if b & 1:
            res ^= a
        a = _xtime(a)
        b >>= 1
    return res


def _mix_columns(state):
    for c in range(4):
        i = 4*c
        a0, a1, a2, a3 = state[i], state[i+1], state[i+2], state[i+3]
        state[i]   = _mul(a0,2) ^ _mul(a1,3) ^ a2 ^ a3
        state[i+1] = a0 ^ _mul(a1,2) ^ _mul(a2,3) ^ a3
        state[i+2] = a0 ^ a1 ^ _mul(a2,2) ^ _mul(a3,3)
        state[i+3] = _mul(a0,3) ^ a1 ^ a2 ^ _mul(a3,2)


def _inv_mix_columns(state):
    for c in range(4):
        i = 4*c
        a0, a1, a2, a3 = state[i], state[i+1], state[i+2], state[i+3]
        state[i]   = _mul(a0,14) ^ _mul(a1,11) ^ _mul(a2,13) ^ _mul(a3,9)
        state[i+1] = _mul(a0,9)  ^ _mul(a1,14) ^ _mul(a2,11) ^ _mul(a3,13)
        state[i+2] = _mul(a0,13) ^ _mul(a1,9)  ^ _mul(a2,14) ^ _mul(a3,11)
        state[i+3] = _mul(a0,11) ^ _mul(a1,13) ^ _mul(a2,9)  ^ _mul(a3,14)


def aes_encrypt_block(block16: bytes, round_keys) -> bytes:
    if len(block16) != 16:
        raise ValueError("AES block must be 16 bytes")

    state = bytearray(block16)
    Nr = 10

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
    Nr = 10

    _add_round_key(state, round_keys[Nr])
    _inv_shift_rows(state)
    _inv_sub_bytes(state)

    for r in range(Nr-1, 0, -1):
        _add_round_key(state, round_keys[r])
        _inv_mix_columns(state)
        _inv_shift_rows(state)
        _inv_sub_bytes(state)

    _add_round_key(state, round_keys[0])
    return bytes(state)
