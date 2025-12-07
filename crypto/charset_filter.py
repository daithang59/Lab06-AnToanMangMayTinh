# crypto/charset_filter.py
"""
Character Set Validation and Filtering
---------------------------------------
Theo yêu cầu đề bài: chỉ xử lý tập ký tự:
- Chữ thường: a-z
- Chữ hoa: A-Z
- Số: 0-9
- Khoảng trắng
- Dấu câu: . , ; : ? ! ' " - ( )

Ký tự khác giữ nguyên hoặc thay thế bằng khoảng trắng (configurable).
"""

import string

# Tập ký tự cho phép theo đề bài
ALLOWED_CHARSET = set(
    string.ascii_lowercase + string.ascii_uppercase + string.digits + " .,;:?!'\"-()"
)


def is_allowed_char(c: str) -> bool:
    """
    Kiểm tra ký tự c có nằm trong tập cho phép không.

    Args:
        c: Ký tự cần kiểm tra (1 ký tự)

    Returns:
        True nếu ký tự được phép, False nếu không
    """
    return c in ALLOWED_CHARSET


def filter_charset(
    text: str, keep_unknown: bool = False, replacement: str = " "
) -> str:
    """
    Lọc text chỉ giữ lại các ký tự được phép theo đề bài.

    Args:
        text: Chuỗi cần lọc
        keep_unknown: Nếu True, giữ nguyên ký tự không cho phép.
                      Nếu False (default), thay thế bằng replacement.
        replacement: Ký tự thay thế cho ký tự không hợp lệ (default: space)

    Returns:
        Chuỗi đã được lọc

    Examples:
        >>> filter_charset("Hello@World#123!")
        'Hello World 123!'

        >>> filter_charset("Café", keep_unknown=True)
        'Café'

        >>> filter_charset("Test™", keep_unknown=False)
        'Test '
    """
    if keep_unknown:
        return text

    result = []
    for c in text:
        if c in ALLOWED_CHARSET:
            result.append(c)
        else:
            result.append(replacement)

    return "".join(result)


def validate_and_filter(
    text: str, cipher_name: str = "cipher"
) -> tuple[bool, str, str]:
    """
    Validate và filter text, trả về (is_valid, filtered_text, warning_message).

    Args:
        text: Text cần validate
        cipher_name: Tên thuật toán (để hiển thị trong warning)

    Returns:
        Tuple (is_valid, filtered_text, warning_message)
        - is_valid: True nếu không có ký tự lạ, False nếu có
        - filtered_text: Text đã được lọc
        - warning_message: Cảnh báo về ký tự bị loại bỏ (nếu có)

    Examples:
        >>> validate_and_filter("Hello World!", "Caesar")
        (True, "Hello World!", "")

        >>> validate_and_filter("Hello™World", "Vigenere")
        (False, "Hello World", "Warning: 1 ký tự không hợp lệ đã bị thay thế...")
    """
    # Đếm số ký tự không hợp lệ
    invalid_chars = set()
    for c in text:
        if c not in ALLOWED_CHARSET:
            invalid_chars.add(c)

    # Filter text
    filtered_text = filter_charset(text, keep_unknown=False, replacement=" ")

    # Tạo warning message nếu có ký tự không hợp lệ
    if invalid_chars:
        invalid_count = sum(1 for c in text if c not in ALLOWED_CHARSET)
        warning = (
            f"⚠️ Phát hiện {invalid_count} ký tự không nằm trong tập cho phép "
            f"(a-z, A-Z, 0-9, space, .,;:?!'\"-(). "
            f"Các ký tự này đã được thay thế bằng khoảng trắng. "
            f"Ký tự bị loại: {', '.join(repr(c) for c in sorted(invalid_chars)[:10])}"
        )
        return False, filtered_text, warning

    return True, filtered_text, ""


def get_charset_info() -> str:
    """
    Trả về thông tin về tập ký tự được phép (để hiển thị trong UI/help).

    Returns:
        Chuỗi mô tả tập ký tự
    """
    return (
        "Tập ký tự được phép:\n"
        "• Chữ cái: a-z, A-Z\n"
        "• Số: 0-9\n"
        "• Khoảng trắng\n"
        "• Dấu câu: . , ; : ? ! ' \" - ( )\n"
        "Các ký tự khác sẽ được thay thế bằng khoảng trắng."
    )


# Test nhanh
if __name__ == "__main__":
    # Test cases
    test_texts = [
        "Hello, World! 123",
        "Café au lait",
        "Test@email.com",
        "Valid: a-z, A-Z, 0-9",
        "Symbols: .,;:?!'\"-()",
    ]

    print("=== Character Set Filter Test ===\n")
    print(get_charset_info())
    print("\n=== Test Cases ===\n")

    for text in test_texts:
        is_valid, filtered, warning = validate_and_filter(text)
        print(f"Original: {text}")
        print(f"Filtered: {filtered}")
        if warning:
            print(f"Warning:  {warning}")
        print()
