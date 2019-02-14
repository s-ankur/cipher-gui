#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unencrypted Plaintext
"""
import string

alphabet = string.printable
cipher_type = 'text'
key_length = 1


def encrypt(plaintext, key):
    return plaintext


decrypt = encrypt


def crack(ciphertext):
    return ciphertext, ''
