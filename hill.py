#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
In classical cryptography, the Hill cipher is a polygraphic substitution cipher based on linear algebra.
Invented by Lester S. Hill in 1929, it was the first polygraphic cipher in which it was practical
(though barely) to operate on more than three symbols at once.
"""
import string
import numpy as np

alphabet = string.ascii_uppercase
cipher_type = string
key_length = 9


def modular_inverse(A, p):
    n = len(A)
    A = np.matrix(A)
    adj = np.zeros(shape=(n, n))
    for i in range(0, n):
        for j in range(0, n):
            adj[i][j] = ((-1)**(i + j) * int(round(np.linalg.det(minor(A, j, i))))) % p
    return (modInv(int(round(np.linalg.det(A))), p) * adj) % p


def modInv(a, p):          # Finds the inverse of a mod p, if it exists
    for i in range(1, p):
        if (i * a) % p == 1:
            return i
    raise ValueError(str(a) + " has no inverse mod " + str(p))


def minor(A, i, j):    # Return matrix A with the ith row and jth column deleted
    A = np.array(A)
    minor = np.zeros(shape=(len(A) - 1, len(A) - 1))
    p = 0
    for s in range(0, len(minor)):
        if p == i:
            p = p + 1
        q = 0
        for t in range(0, len(minor)):
            if q == j:
                q = q + 1
            minor[s][t] = A[p][q]
            q = q + 1
        p = p + 1
    return minor


def check_mod_inv(matrix):
    for i in range(100):
        try:
            modular_inverse(matrix, 26).astype(int)
            break
        except:
            np.random.seed(matrix.sum())
            matrix = np.random.randint(0, 25, (3, 3))
    return matrix


def create_matrix(key):
    matrix = np.array(list(map(ord, key))) - ord('A')
    matrix = matrix.reshape(3, 3)
    matrix = check_mod_inv(matrix)
    return matrix


def encrypt(plaintext, key):
    key = key.upper()
    key = key[:9] + 'X' * (9 - len(key))
    d = len(plaintext) % 3
    rem = plaintext[-d:]
    plaintext = plaintext.upper()[:-d]
    txt = np.array(list(map(ord, plaintext))) - ord('A')
    txt = txt.reshape(3, -1)
    key = create_matrix(key)
    cip = (key@txt) % 26
    cip = cip.reshape(-1) + ord('A')
    return ''.join(list(map(chr, cip))) + rem


def decrypt(ciphertext, key):
    key = key.upper()
    key = key[:9] + 'X' * (9 - len(key))
    d = len(ciphertext) % 3
    rem = ciphertext[-d:]
    ciphertext = ciphertext.upper()[:-d]
    txt = np.array(list(map(ord, ciphertext))) - ord('A')
    txt = txt.reshape(3, -1)
    key = create_matrix(key)
    key = modular_inverse(key, 26).astype(int)
    cip = (key@txt) % 26
    cip = cip.reshape(-1) + ord('A')
    return ''.join(list(map(chr, cip))).strip() + rem
