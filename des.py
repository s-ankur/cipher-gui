#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
DES CIPHER
The Data Encryption Standard is a symmetric-key algorithm
for the encryption of electronic data. Although its short key length of 56 bits,
criticized from the beginning, makes it too insecure for most current applications,
it was highly influential in the advancement of modern cryptography.
"""
from des_blocks import *

cipher_type = 'block'

N_ROUNDS = 16


def binvalue(val, bitsize):
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise "binary value larger than the expected size"
    while len(binval) < bitsize:
        binval = "0" + binval
    return binval


def nsplit(s, n):
    return [s[k:k + n] for k in range(0, len(s), n)]


def remove_padding(data):
    pad_len = ord(data[-1])
    return data[:-pad_len]


def substitute(d_e):
    subblocks = nsplit(d_e, 6)
    result = list()
    for i in range(len(subblocks)):
        block = subblocks[i]
        row = int(str(block[0]) + str(block[5]), 2)
        column = int(''.join([str(x) for x in block[1:][:-1]]), 2)
        val = S_BOX[i][row][column]
        bin = binvalue(val, 4)
        result += [int(x) for x in bin]
    return result


def xor(t1, t2):
    return [x ^ y for x, y in zip(t1, t2)]


def shift(g, d, n):
    return g[n:] + g[:n], d[n:] + d[:n]


def permute(block, table):
    return [block[x - 1] for x in table]


def add_padding(text):
    pad_len = len(text) % 8
    text += pad_len * chr(pad_len)
    return text


def validate_text(text):
    if len(text) % 8 != 0:
        raise Exception("Data size should be multiple of 8")


def validate_key(key):
    if len(key) < 8:
        raise Exception("Key Should be 8 bytes long")
    return (key[:8])


def generate_keys(key):
    key = validate_key(key)
    key = string_to_bit_array(key)
    key = permute(key, CP_1)
    left, right = nsplit(key, 28)
    for i in range(N_ROUNDS):
        left, right = shift(left, right, SHIFT[i])
        yield permute(left + right, CP_2)


def string_to_bit_array(text):  # Convert a string into a list of bits
    array = list()
    for char in text:
        binval = binvalue(char, 8)  # Get the char value on one byte
        array.extend([int(x) for x in list(binval)])  # Add the bits to the final list
    return array


def bit_array_to_string(array):  # Recreate the string from the bit array
    res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in bytes]) for bytes in nsplit(array, 8)]])
    return res


def block_iter(block, keys):
    left, right = nsplit(block, 32)
    for key in keys:
        right_expanded = permute(right, E)
        d_e = right_expanded
        tmp = xor(key, right_expanded)
        tmp = substitute(tmp)
        tmp = permute(tmp, P)
        tmp = xor(left, tmp)
        left = right
        right = tmp
        yield right + left


def feistel_network(text, keys):
    text_blocks = nsplit(text, 8)
    text_output = []
    for text_block in text_blocks:
        block = string_to_bit_array(text_block)
        block = permute(block, P_INITIAL)
        bi = list(block_iter(block, keys))
        block = bi[-1]
        block = permute(block, P_INITIAL_1)
        text_block = bit_array_to_string(block)
        text_output.append(text_block)
    return ''.join(text_output)


def encrypt(plaintext, key):
    plaintext = add_padding(plaintext)
    keys = list(generate_keys(key))
    return feistel_network(plaintext, keys)


def decrypt(ciphertext, key):
    keys = list(generate_keys(key))
    keys.reverse()
    plaintext = feistel_network(ciphertext, keys)
    return (plaintext)
