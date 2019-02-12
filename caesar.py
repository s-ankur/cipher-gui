#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Caesar shift, is one of the simplest and most widely known encryption techniques.
It is a type of substitution cipher in which each letter in the plaintext is replaced
by a letter some fixed number of positions down the alphabet. For example,
with a left shift of 3, D would be replaced by A, E would become B, and so on.
The method is named after Julius Caesar, who used it in his private correspondence.
"""
from collections import Counter
from functools import lru_cache
import string

FREQ_LETTERS = 'ETAOINSRHDLUCMFYWGPBVKXQJZ'

cipher_type = 'text'
alphabet = string.printable

def encrypt_letter(letter, key):
    if letter.islower():
        return chr((ord(letter) + key - ord('a')) % 26 + ord('a'))
    if letter.isupper():
        return chr((ord(letter) + key - ord('A')) % 26 + ord('A'))
    return letter


def encrypt(plaintext, key):
    key = ord(key.lower()[0]) - ord('a')
    return ''.join(list(map(lambda x: encrypt_letter(x, key), plaintext)))


def decrypt(ciphertext, key):
    key = - (ord(key.lower()[0]) - ord('a'))
    return ''.join(list(map(lambda x: encrypt_letter(x, key), ciphertext)))


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    L = [[None] * (n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L[m][n]


def crack(ciphertext):
    ciphertext_orig = ciphertext
    ciphertext = ciphertext.upper()
    candidates = []
    for candidate_key in string.ascii_lowercase:
        print('trying', candidate_key)
        candidate_plaintext = decrypt(ciphertext, candidate_key)
        freq_cipher = ''.join([letter for letter, count in Counter(candidate_plaintext).most_common() if letter.isalpha()])
        print(freq_cipher)
        candidates.append((lcs(freq_cipher, FREQ_LETTERS), candidate_key))
    key = max(candidates)[1]
    plaintext = decrypt(ciphertext_orig, key)
    return plaintext, key
