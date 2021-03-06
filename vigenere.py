#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
The Vigenère cipher is a method of encrypting alphabetic text by using a
series of interwoven Caesar ciphers, based on the letters of a keyword.
It is a form of polyalphabetic substitution.
"""
import random
from itertools import cycle
from collections import Counter
import caesar
import test

cipher_type = 'text'


def encrypt(plaintext, key):
    key = map(lambda x: ord(x) - ord('a'), key.lower())
    return ''.join(list(map(lambda p: caesar.encrypt_letter(*p), zip(plaintext, cycle(key)))))


def decrypt(ciphertext, key):
    key = map(lambda x: -(ord(x) - ord('a')), key.lower())
    return ''.join(list(map(lambda x: caesar.encrypt_letter(*x), zip(ciphertext, cycle(key)))))


def crack(ciphertext):
    length = test.kasiski_length(ciphertext)
    length = random.choice([int(length), int(length) + 1])
    key = []
    for i in range(length):
        column = ciphertext[i::length]
        text, key_letter = caesar.crack(column)
        key.append(key_letter)
    key = ''.join(key)
    plaintext = decrypt(ciphertext, key)
    return plaintext, key
