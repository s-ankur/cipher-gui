#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Common Testing Program for all ciphers
"""
import string
import random
from collections import Counter
import time
from pprint import pprint
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

ENGLISH_FREQ = Counter({
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.0236,
    'X': 0.0015,
    'Y': 0.01974,
    'Z': 0.00074,
})


def gen_text(n=160,alphabet = string.ascii_uppercase):
    return "".join(random.choices(alphabet,k=n))

def gen_key(n=8,alphabet = string.ascii_letters):
    return gen_text(n,alphabet)

def gen_block(n=8):
    return random.getrandbits(n * 8)

def get_freq(text):
    freq = Counter(string.ascii_uppercase)
    freq.update(filter(str.isupper, text.upper()))
    n = len(text)
    for i in freq:
        freq[i] -= 1
    return freq.most_common()

def number_to_block(number):
    block = [(number // (1 << i)) % 2 for i in range(64)]
    block.reverse()
    return block

def correctness(cipher):
    start = time.time()
    incorrect = []
    for i in range(10):
        plaintext = gen_text()
        key = gen_key()
        ciphertext = cipher.encrypt(plaintext, key)
        decrypttext = cipher.decrypt(ciphertext, key)
        if decrypttext != plaintext:
            incorrect.append({'plaintext': plaintext, 'key': key, 'ciphertext': ciphertext, 'decrypttext': decrypttext})
    return {'score': (100-len(incorrect)) , 'incorrect':incorrect,'time':time.time()-start}


def simmons(cipher,):
    plaintext = ''.join(random.choices(list(ENGLISH_FREQ.keys()), list(ENGLISH_FREQ.values()), k=100000))
    key = gen_key()
    ciphertext = cipher.encrypt(plaintext, key)
    plaintext_freq = ENGLISH_FREQ.most_common()
    ciphertext_freq = get_freq(ciphertext)
    plaintext_freq = get_freq(plaintext)
    max_plaintext_freq = max(plaintext_freq,key = lambda x:x[1])[1]
    score = 0
    for (freq_p, freq_c) in zip(plaintext_freq, ciphertext_freq):
        score += abs(freq_p[1] - freq_c[1])
    relative_freq = list(map(lambda x:x[1]/max_plaintext_freq,ciphertext_freq))
    return {'score': score/700, 'ciphertext_freq': ciphertext_freq, 'plaintext': plaintext,'relative_freq':relative_freq}


def avalanche(cipher):
    block = gen_block()
    key = gen_key(8,)
    keys = list(cipher.generate_keys(key))
    bit_n = random.randint(0, 63)
    block_altered = block ^ (1 << bit_n)
    block = number_to_block(block)
    block_altered = number_to_block(block_altered)
    flips = []
    for i, j in zip(cipher.block_iter(block, keys), cipher.block_iter(block_altered, keys)):
        flips.append(len(list(filter(lambda a: a[0] != a[1], zip(i, j)))))
    return {'score':sum(flips)/16,'flips': flips}


if __name__ == '__main__':
    from main import AVAILABLE_CIPHERS
    for cipher in AVAILABLE_CIPHERS:
        try:
            cipher_module = __import__(cipher)
            result = correctness(cipher_module)
            print("Cipher %s passed correctness with score %d%%"%(cipher,result['score']))
            if cipher_module.cipher_type == 'block':
                result = (avalanche(cipher_module))
                print("Cipher %s passed avalanche with score %d"%(cipher,result['score']))
                plt.figure('Avalanche')
                plt.bar(range(len(result['flips'])), result['flips'])
            else:
                result = simmons(cipher_module)
                print("Cipher %s passed simmons with score %d"%(cipher,result['score']))
                plt.figure('Simmons')
                plt.plot(result['relative_freq'], label=cipher)
                plt.legend()
        except Exception as e:
            raise
            print("Cipher %s caused exception",str(e))

    plt.show()
