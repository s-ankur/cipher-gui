#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
The Atbash cipher is a particular type of monoalphabetic cipher formed by taking the
alphabet (or abjad, syllabary, etc.) and mapping it to its reverse, so that the first
letter becomes the last letter, the second letter becomes the second to last letter, and so on
'a' -> 'z' , 'b' -> 'y' etc
"""


import string

cipher_type = 'text'
cipher_alphabet = string.printable
key_length = 1


def encrypt_letter(letter):
    if letter.islower():
        return string.ascii_lowercase[-(1 + string.ascii_lowercase.index(letter))]
    elif letter.isupper():
        return string.ascii_uppercase[-(1 + string.ascii_uppercase.index(letter))]
    return letter


def encrypt(plaintext, key=''):
    return ''.join(list(map(encrypt_letter, plaintext)))


decrypt = encrypt


def crack(plaintext):
    return encrypt(plaintext), ''
