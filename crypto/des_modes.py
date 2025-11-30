# crypto/des_modes.py
"""
DES modes (ECB, CBC) with PKCS#7 padding
----------------------------------------
API:
- des_encrypt(plaintext: bytes, key: bytes, mode: str, iv: bytes|None)
    -> (ciphertext: bytes, iv_used: bytes|None)
- des_decrypt(ciphertext: bytes, key: bytes, mode: str, iv: bytes|None)
    -> plaintext: bytes
"""

import os
from .des_core import des_key_schedule, des_encrypt_block, des_decrypt_block

BLOCK_SIZE = 8


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


def _ecb_encrypt(plaintext: bytes, subkeys) -> bytes:
    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE)
    out = []
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        out.append(des_encrypt_block(block, subkeys))
    return b"".join(out)


def _ecb_decrypt(ciphertext: bytes, subkeys) -> bytes:
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext length not multiple of block size")
    out = []
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        out.append(des_decrypt_block(block, subkeys))
    return pkcs7_unpad(b"".join(out))


def _cbc_encrypt(plaintext: bytes, subkeys, iv: bytes) -> (bytes, bytes):
    if iv is None:
        iv = os.urandom(BLOCK_SIZE)
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be 8 bytes for DES CBC")
    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE)
    out = []
    prev = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        x = bytes(a ^ b for a, b in zip(block, prev))
        c = des_encrypt_block(x, subkeys)
        out.append(c)
        prev = c
    return b"".join(out), iv


def _cbc_decrypt(ciphertext: bytes, subkeys, iv: bytes) -> bytes:
    if iv is None or len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be 8 bytes for DES CBC decryption")
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext length not multiple of block size")

    out = []
    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        x = des_decrypt_block(block, subkeys)
        p = bytes(a ^ b for a, b in zip(x, prev))
        out.append(p)
        prev = block
    return pkcs7_unpad(b"".join(out))


def des_encrypt(plaintext: bytes, key: bytes, mode: str, iv: bytes = None):
    """Main API for Flask."""
    if len(key) != 8:
        raise ValueError("DES key must be 8 bytes")
    subkeys = des_key_schedule(key)
    mode = mode.upper()

    if mode == "ECB":
        c = _ecb_encrypt(plaintext, subkeys)
        return c, None
    elif mode == "CBC":
        c, iv_used = _cbc_encrypt(plaintext, subkeys, iv)
        return c, iv_used
    else:
        raise ValueError("Unsupported DES mode: " + mode)


def des_decrypt(ciphertext: bytes, key: bytes, mode: str, iv: bytes = None):
    """Main API for Flask."""
    if len(key) != 8:
        raise ValueError("DES key must be 8 bytes")
    subkeys = des_key_schedule(key)
    mode = mode.upper()

    if mode == "ECB":
        return _ecb_decrypt(ciphertext, subkeys)
    elif mode == "CBC":
        return _cbc_decrypt(ciphertext, subkeys, iv)
    else:
        raise ValueError("Unsupported DES mode: " + mode)
