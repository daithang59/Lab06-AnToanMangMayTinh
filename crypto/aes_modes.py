# crypto/aes_modes.py
"""
AES modes (ECB, CBC) with PKCS#7
--------------------------------
- aes_encrypt(plaintext, key, mode, iv=None) -> (ciphertext, iv_used)
- aes_decrypt(ciphertext, key, mode, iv=None) -> plaintext
"""

import os
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
        block = plaintext[i:i+BLOCK_SIZE]
        out.append(aes_encrypt_block(block, round_keys))
    return b"".join(out)


def _ecb_decrypt(ciphertext: bytes, round_keys) -> bytes:
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext length not multiple of block size")
    out = []
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        out.append(aes_decrypt_block(block, round_keys))
    return pkcs7_unpad(b"".join(out))


def _cbc_encrypt(plaintext: bytes, round_keys, iv: bytes) -> (bytes, bytes):
    if iv is None:
        iv = os.urandom(BLOCK_SIZE)
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be 16 bytes for AES CBC")
    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE)
    out = []
    prev = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
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
        block = ciphertext[i:i+BLOCK_SIZE]
        x = aes_decrypt_block(block, round_keys)
        p = bytes(a ^ b for a, b in zip(x, prev))
        out.append(p)
        prev = block
    return pkcs7_unpad(b"".join(out))


def aes_encrypt(plaintext: bytes, key: bytes, mode: str, iv: bytes = None):
    """
    Main API cho Flask.
    key: 16 bytes (AES-128)
    """
    if len(key) != 16:
        raise ValueError("AES-128 key must be 16 bytes")

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
    if len(key) != 16:
        raise ValueError("AES-128 key must be 16 bytes")

    round_keys = key_expansion(key)
    mode = mode.upper()

    if mode == "ECB":
        return _ecb_decrypt(ciphertext, round_keys)
    elif mode == "CBC":
        return _cbc_decrypt(ciphertext, round_keys, iv)
    else:
        raise ValueError("Unsupported AES mode: " + mode)
