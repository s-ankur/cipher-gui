#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
The Atbash cipher is a particular type of monoalphabetic cipher formed by taking the
alphabet (or abjad, syllabary, etc.) and mapping it to its reverse, so that the first
letter becomes the last letter, the second letter becomes the second to last letter, and so on
'a' -> 'z' , 'b' -> 'y' etc
"""


import string


def encrypt_letter(letter):
    if char in string.ascii_lowercase:
        return string.ascii_lowercase[-(1 + string.ascii_lowercase.index(char))]
    elif char in string.ascii_uppercase:
        return string.ascii_uppercase[-(1 + string.ascii_uppercase.index(char))]
    return char


def encrypt(plaintext, key=''):
    return ''.join(list(map(encrypt_letter, plaintext)))


decrypt = crack = encrypt
