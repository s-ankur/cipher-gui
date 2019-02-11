#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
The Vigenère cipher is a method of encrypting alphabetic text by using a
series of interwoven Caesar ciphers, based on the letters of a keyword.
It is a form of polyalphabetic substitution.
"""
from itertools import cycle
from collections import Counter
import caesar

Kp = 0.067
Kt = 0.0385

cipher_type = 'text'


def encrypt(plaintext, key):
    key = map(lambda x: ord(x) - ord('a'), key.lower())
    return ''.join(list(map(lambda p: caesar.encrypt_letter(*p), zip(plaintext, cycle(key)))))


def decrypt(ciphertext, key):
    key = map(lambda x: -(ord(x) - ord('a')), key.lower())
    return ''.join(list(map(lambda x: caesar.encrypt_letter(*x), zip(ciphertext, cycle(key)))))


def crack(ciphertext):
    ciphertext_freq = Counter(filter(str.isalpha, ciphertext.lower()))
    N = sum(ciphertext_freq.values())
    sigma = sum(map(lambda freq: freq * (freq - 1), ciphertext_freq.values()))
    Ko = sigma / (N * (N - 1))
    length = (Kp - Kt) / (Ko - Kt)
    length = round(length)
    key = []
    for i in range(length):
        column = ciphertext[i::length]
        text, key_letter = caesar.crack(column)
        key.append(key_letter)
    key = ''.join(key)
    plaintext = decrypt(ciphertext, key)
    return plaintext, key
