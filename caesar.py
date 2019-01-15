#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Caesar shift, is one of the simplest and most widely known encryption techniques.
It is a type of substitution cipher in which each letter in the plaintext is replaced
by a letter some fixed number of positions down the alphabet. For example,
with a left shift of 3, D would be replaced by A, E would become B, and so on.
The method is named after Julius Caesar, who used it in his private correspondence.
"""


def encrypt_letter(letter, key):
    if letter.islower():
        return chr((ord(letter) + key - ord('a')) % 26 + ord('a'))
    if letter.isupper():
        return chr((ord(letter) + key - ord('A')) % 26 + ord('A'))
    return letter


def encrypt(plaintext, key):
    key = ord(key.lower())-ord('a')
    return ''.join(list(map(lambda x: encrypt_letter(x, key), plaintext)))

def decrypt(ciphertext, key):
    key = - (ord(key.lower())-ord('a'))
    return ''.join(list(map(lambda x: encrypt_letter(x, key), ciphertext)))
