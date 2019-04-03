from math import sqrt
from time import time
from itertools import islice
from statistics import mean,stdev
from scipy.stats import chi2,norm
import numpy as np
import matplotlib.pyplot as plt
from Crypto.Cipher import DES3
from Crypto import Random
from Crypto.Util.strxor import strxor


def lcg(initial = 1, constants =[3,1], m=31 ):
    rand = initial
    a,c =constants
    while True:
        rand = (a * rand + c) % m
        yield rand / m


def ansi(initial = Random.new().read(8) , constants = [Random.new().read(16)]):
    V = initial
    key = constants[0]
    des3 = DES3.new(key, DES3.MODE_ECB)
    while True:
        EDT = des3.encrypt(hex(int(time() * 10**6))[-8:])
        R = des3.encrypt(strxor(V, EDT))
        V = des3.encrypt(strxor(R, EDT))
        yield int(V.hex(), 16)


def bbs(initial =101355, constants =  [383,503]):
    s = initial
    p, q = constants
    n = p * q
    x = (s * s) % n
    while True:
        x = (x * x) % n
        b = x % 2
        yield x / n


def spectral(numbers):
    plt.scatter(numbers[1:], numbers[:-1])
    plt.show()


def count(list1, l, r):
    c = 0
    for x in list1:
        if x >= l and x <= r:
            c += 1
    return c


def chisquare(numbers, alpha=0.01, k=10):
    counts = []
    for i in range(k):
        counts.append(count(numbers, (i / k), (i + 1) /k))
    d = 0
    l = len(numbers)
    exp = l / k
    for i in range(k):
        err = (counts[i] - exp)**2
        d += err / exp
    stat = d
    critical = chi2.ppf(1 - alpha, k - 1)
    if abs(stat) >= critical:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')

def ks_test(numbers):
    average = mean(numbers)
    dev = stdev(numbers)
    l = len(numbers)
    for i in range(l):
        numbers[i] = (numbers[i] - average) / dev
    numbers.sort()
    normal = []
    diff = []
    for i in range(l):
        normal.append(norm.cdf(numbers[i]))
        diff.append(abs((i + 1) / l - normal[i]))
    d = max(diff)
    critical = 1.36 / sqrt(n)
    if d >= critical:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')

if __name__ == "__main__":
    n =1000
    lcg_numbers=list(islice(lcg(),n))
    bbs_numbers=list(islice(bbs(),n))
    ansi_numbers=list(islice(ansi(),n))
    spectral(lcg_numbers)
    for numbers in lcg_numbers,bbs_numbers,ansi_numbers:
        ks_test(numbers)
        chisquare(numbers)

    
