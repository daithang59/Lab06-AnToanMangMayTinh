# crypto/aes_modes.py
"""
AES modes (ECB, CBC) with PKCS#7
--------------------------------
- aes_encrypt(plaintext, key, mode, iv=None) -> (ciphertext_bytes, iv_used)
- aes_decrypt(ciphertext_bytes, key, mode, iv=None) -> plaintext_bytes

- encrypt(plaintext_bytes, key, mode, iv=None, out_format='hex') -> (ciphertext_str, iv_used)
- decrypt(ciphertext_str_or_bytes, key, mode, iv, in_format='hex') -> plaintext_bytes

Hỗ trợ key:
- 16 bytes: AES-128
- 24 bytes: AES-192
- 32 bytes: AES-256

Block size luôn 16 bytes (128 bit) theo chuẩn AES.
"""

import os
import base64
from .aes_core import key_expansion, aes_encrypt_block, aes_decrypt_block

BLOCK_SIZE = 16


def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        raise ValueError("Invalid padding (empty data)")
    pad_len = data[-1]
    if pad_len <= 0 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding length")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid PKCS#7 padding")
    return data[:-pad_len]


def _ecb_encrypt(plaintext: bytes, round_keys) -> bytes:
    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE)
    out = []
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i : i + BLOCK_SIZE]
        out.append(aes_encrypt_block(block, round_keys))
    return b"".join(out)


def _ecb_decrypt(ciphertext: bytes, round_keys) -> bytes:
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext length not multiple of block size")
    out = []
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i : i + BLOCK_SIZE]
        out.append(aes_decrypt_block(block, round_keys))
    return pkcs7_unpad(b"".join(out))


def _cbc_encrypt(plaintext: bytes, round_keys, iv: bytes):
    if iv is None:
        iv = os.urandom(BLOCK_SIZE)
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be 16 bytes for AES CBC")
    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE)
    out = []
    prev = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i : i + BLOCK_SIZE]
        x = bytes(a ^ b for a, b in zip(block, prev))
        c = aes_encrypt_block(x, round_keys)
        out.append(c)
        prev = c
    return b"".join(out), iv


def _cbc_decrypt(ciphertext: bytes, round_keys, iv: bytes) -> bytes:
    if iv is None or len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be 16 bytes for AES CBC decryption")
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext length not multiple of block size")

    out = []
    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i : i + BLOCK_SIZE]
        x = aes_decrypt_block(block, round_keys)
        p = bytes(a ^ b for a, b in zip(x, prev))
        out.append(p)
        prev = block
    return pkcs7_unpad(b"".join(out))


# ========== Lõi bytes-in / bytes-out cho backend / test ==========
def aes_encrypt(plaintext: bytes, key: bytes, mode: str, iv: bytes = None):
    """
    Main API bytes-in/bytes-out.
    key: 16 / 24 / 32 bytes (AES-128/192/256)
    mode: 'ECB' hoặc 'CBC'
    """
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes")

    round_keys = key_expansion(key)
    mode = mode.upper()

    if mode == "ECB":
        c = _ecb_encrypt(plaintext, round_keys)
        return c, None
    elif mode == "CBC":
        c, iv_used = _cbc_encrypt(plaintext, round_keys, iv)
        return c, iv_used
    else:
        raise ValueError("Unsupported AES mode: " + mode)


def aes_decrypt(ciphertext: bytes, key: bytes, mode: str, iv: bytes = None):
    """
    Main API bytes-in/bytes-out cho giải mã.
    """
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes")

    round_keys = key_expansion(key)
    mode = mode.upper()

    if mode == "ECB":
        return _ecb_decrypt(ciphertext, round_keys)
    elif mode == "CBC":
        return _cbc_decrypt(ciphertext, round_keys, iv)
    else:
        raise ValueError("Unsupported AES mode: " + mode)


# ===== Wrapper theo đúng API của đề: encrypt / decrypt (hex/Base64) =====
def encrypt(
    plaintext: bytes, key: bytes, mode: str, iv: bytes = None, out_format: str = "hex"
):
    """
    encrypt(plaintext, key, mode, iv=None) -> ciphertext (chuỗi hex/base64)

    - plaintext: dữ liệu gốc (bytes)
    - key: 16 / 24 / 32 bytes (AES-128/192/256)
    - mode: 'ECB' hoặc 'CBC'
    - iv: 16 bytes hoặc None (CBC không có iv -> tự generate)
    - out_format: 'hex' hoặc 'base64'

    Trả về:
        (ciphertext_str, iv_used)
        - ciphertext_str: chuỗi hex hoặc base64
        - iv_used: iv thật sự (bytes), None nếu ECB
    """
    raw_ct, iv_used = aes_encrypt(plaintext, key, mode, iv)

    fmt = out_format.lower()
    if fmt == "hex":
        ct_str = raw_ct.hex()
    elif fmt in ("b64", "base64"):
        ct_str = base64.b64encode(raw_ct).decode("ascii")
    else:
        raise ValueError("Unsupported output format (use 'hex' or 'base64')")

    return ct_str, iv_used


def decrypt(
    ciphertext, key: bytes, mode: str, iv: bytes, in_format: str = "hex"
) -> bytes:
    """
    decrypt(ciphertext, key, mode, iv) -> plaintext

    - ciphertext:
        + nếu in_format = 'hex' hoặc 'base64'  -> ciphertext là str
        + nếu in_format = 'raw'                -> ciphertext là bytes
    - key: 16 / 24 / 32 bytes
    - mode: 'ECB' hoặc 'CBC'
    - iv: 16 bytes (bắt buộc cho CBC)
    - in_format: 'hex' | 'base64' | 'raw'

    Trả về:
        plaintext: bytes
    """
    if isinstance(ciphertext, str):
        fmt = in_format.lower()
        if fmt == "hex":
            raw_ct = bytes.fromhex(ciphertext.strip())
        elif fmt in ("b64", "base64"):
            raw_ct = base64.b64decode(ciphertext)
        else:
            raise ValueError(
                "If ciphertext is str, in_format must be 'hex' or 'base64'"
            )
    else:
        # ciphertext là bytes
        if in_format.lower() != "raw":
            raise ValueError("If ciphertext is bytes, use in_format='raw'")
        raw_ct = ciphertext

    return aes_decrypt(raw_ct, key, mode, iv)
