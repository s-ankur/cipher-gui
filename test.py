#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Common Testing Program for all ciphers
"""
import string
import random


def test(cipher):
    plaintext = "".join([random.choice(string.printable) for i in range(100)] )
    key = "".join([random.choice(string.ascii_letters) for i in range(10)] )
    ciphertext=cipher.encrypt(plaintext,key)
    decrypttext = cipher.decrypt(ciphertext,key)
    return decrypttext ==plaintext,plaintext,key
    

if __name__ == '__main__':
    from main import AVAILABLE_CIPHERS

    for cipher in AVAILABLE_CIPHERS:
        cipher_module = __import__(cipher)
        for i in range(100):
            status,plaintext,key = test(cipher_module)
            if not status:
                print('Cipher %s Failed Test (%s,%s)'%(cipher,plaintext,key))
        print('Tested',cipher)
    print('Tests Completed')
