#!/usr/bin/python3
# -*- coding: utf-8 -*-
import string

# ATBASH CIPHER
# 'a' -> 'z' , 'b' -> 'y' etc


def encrypt_char_atbash(char):
    if char in string.ascii_lowercase:
        return string.ascii_lowercase[-(1 + string.ascii_lowercase.index(char))]
    elif char in string.ascii_uppercase:
        return string.ascii_uppercase[-(1 + string.ascii_uppercase.index(char))]
    return char


def encrypt(plaintext):
    return ''.join(list(map(encrypt_char_atbash, plaintext)))


decrypt = encrypt
