# -*- coding: utf-8 -*-
"""
Verhoeff Checksum Algorithm
Standard checksum algorithm used for validating 12-digit Indian Aadhaar Numbers.
"""

_D_TABLE = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]

_P_TABLE = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

_INV_TABLE = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

def validate_verhoeff(num_str: str) -> bool:
    cleaned = ''.join(c for c in str(num_str) if c.isdigit())
    if not cleaned or len(cleaned) < 2:
        return False
    c = 0
    reversed_digits = [int(x) for x in reversed(cleaned)]
    for i, digit in enumerate(reversed_digits):
        c = _D_TABLE[c][_P_TABLE[i % 8][digit]]
    return c == 0

def generate_verhoeff(num_str: str) -> str:
    cleaned = ''.join(c for c in str(num_str) if c.isdigit())
    if not cleaned:
        raise ValueError('Input must contain digits')
    c = 0
    reversed_digits = [int(x) for x in reversed(cleaned)]
    for i, digit in enumerate(reversed_digits):
        c = _D_TABLE[c][_P_TABLE[(i + 1) % 8][digit]]
    check_digit = _INV_TABLE[c]
    return cleaned + str(check_digit)
