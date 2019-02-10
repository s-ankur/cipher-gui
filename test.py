#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Common Testing Program for all ciphers
"""
import string
import random
from collections import Counter

ENGLISH_FREQ = Counter({
    'A':0.08167,
    'B':0.01492,
    'C':0.02782,
    'D':0.04253,
    'E':0.12702,
    'F':0.02228,
    'G':0.02015,
    'H':0.06094,
    'I':0.06966,
    'J':0.00153,
    'K':0.00772,
    'L':0.04025,
    'M':0.02406,
    'N':0.06749,
    'O':0.07507,
    'P':0.01929,
    'Q':0.00095,
    'R':0.05987,
    'S':0.06327,
    'T':0.09056,
    'U':0.02758,
    'V':0.00978,
    'W':0.0236,
    'X':0.0015,
    'Y':0.01974,
    'Z':0.00074,
})

def gen_text(n=100):
    return "".join([random.choice(string.printable) for i in range(n)])

def gen_key(n=10):
    return "".join([random.choice(string.ascii_letters) for i in range(n)])

def get_freq(text):
    c= Counter(filter(str.isalpha,text.upper()))
    n = len(text)
    for i in c:
        c[i]/=n
    return c.most_common()

def gen_block(n=8):
    return random.getrandbits(n*8)

def correctness(cipher):
    plaintext = gen_text()
    key = gen_key()
    ciphertext = cipher.encrypt(plaintext,key)
    decrypttext = cipher.decrypt(ciphertext, key)
    return {'passed':decrypttext == plaintext , 'plaintext':plaintext, 'key':key,'ciphertext':ciphertext,'decrypttext':decrypttext}

def simmons(cipher):
    key=gen_key()
    plaintext = ''.join(random.choices(list(ENGLISH_FREQ.keys()),list(ENGLISH_FREQ.values()),k=100))
    ciphertext = cipher.encrypt(plaintext, key)
    plaintext_freq = ENGLISH_FREQ.most_common()
    ciphertext_freq = get_freq(ciphertext)
    diff=0
    for (freq_p,freq_c) in zip(plaintext_freq,ciphertext_freq):
        diff+=abs(freq_p[1]-freq_c[1])
    return {'diff':diff,'freq':ciphertext_freq}
    
def avalanche(cipher):
    block=gen_block()
    key=gen_key(8)
    keys=cipher.generate_keys(key)
    bit_n = random.randint(0,63)
    block_altered = block^(1<<bit_n)
    diff=[]
    for i,j in zip(cipher.block_iter(block,keys),cipher.block_iter(block_altered,keys)):
        diff.append(bin(i^j).count('1'))
    return {'diff',diff}

    
if __name__ == '__main__':
    from main import AVAILABLE_CIPHERS
    for cipher in AVAILABLE_CIPHERS:
        cipher_module = __import__(cipher)
        for i in range(100):
            result=correctness(cipher_module)
            if not result['passed']:
                print(result)
                break
        else:
            print(cipher,'Passed Correctness')
        if cipher_module.cipher_type == 'text':
            print(simmons(cipher_module))
        else:
            print(avalanche(cipher_module))

