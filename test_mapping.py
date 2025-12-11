#!/usr/bin/env python3
"""Test mapping parse logic"""

from crypto.substitution import break_substitution

# Test với text ngắn
test_text = "HELLO WORLD THIS IS A TEST"

print("Testing substitution cipher breaking...")
print(f"Input: {test_text}\n")

score, mapping_str, plaintext = break_substitution(test_text)

print(f"Score: {score}")
print(f"Mapping string from break_substitution():")
print(f"  '{mapping_str}'")
print(f"  Type: {type(mapping_str)}")
print(f"  Length: {len(mapping_str)}")
print()

# Parse logic (same as app.py)
plain_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

print("Parsing mapping_str...")
print(f"Contains pipe: {'|' in mapping_str}")

if "|" in mapping_str:
    parts = mapping_str.split("|")
    print(f"Parts after split: {parts}")
    print()

    for i, part in enumerate(parts):
        part_lower = part.lower().strip()
        print(f"Part {i}: '{part}'")
        print(f"  Lower stripped: '{part_lower}'")

        if part_lower.startswith("plain"):
            plain_alphabet = part.split(":")[-1].strip().upper()
            print(f"  -> Extracted PLAIN: '{plain_alphabet}'")
        elif part_lower.startswith("cipher"):
            cipher_alphabet = part.split(":")[-1].strip().upper()
            print(f"  -> Extracted CIPHER: '{cipher_alphabet}'")
        print()

print("Final results:")
print(f"  cipher_alphabet: '{cipher_alphabet}'")
print(f"  plain_alphabet: '{plain_alphabet}'")
print(f"  plaintext: {plaintext[:100]}...")
