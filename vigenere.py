#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" 
The Vigenère cipher is a method of encrypting alphabetic text by using a
series of interwoven Caesar ciphers, based on the letters of a keyword.
It is a form of polyalphabetic substitution.
"""
from itertools import cycle
import caesar


def encrypt(plaintext, key):
    key= map(lambda x: ord(x)-ord('a'),key.lower())
    return ''.join(list(map(lambda p:caesar.encrypt_letter(*p), zip(plaintext,cycle(key)))))   


def decrypt(ciphertext, key):
    key= map(lambda x: -(ord(x)-ord('a')),key.lower())
    return ''.join(list(map(lambda x:caesar.encrypt_letter(*x), zip(ciphertext,cycle(key)))))
