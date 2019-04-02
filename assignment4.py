import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.stats import norm
from scipy.stats import kstest
from statistics import mean
from statistics import stdev
from math import sqrt
from itertools import islice
from Crypto.Cipher import DES3
from Crypto import Random
from Crypto.Util.strxor import strxor
from scipy.stats import chi2
from time import time


def lcg(a=3, c=1, m=31, rand=1):
    while True:
        rand = (a * rand + c) % m
        yield rand, rand / m


def ansi_x9_17(V, key):
    des3 = DES3.new(key, DES3.MODE_ECB)
    while True:
        EDT = des3.encrypt(hex(int(time() * 10**6))[-8:])
        R = des3.encrypt(strxor(V, EDT))
        V = des3.encrypt(strxor(R, EDT))
        yield int(V.hex(), 16)


def bbs(s=101355, p=383, q=503):
    n = p * q
    x = (s * s) % n
    while True:
        x = (x * x) % n
        b = x % 2
        yield x, x / n, b


n = 250
ls3 = []
ls1 = []
ls4 = []
for i, j in zip(range(n), lcg(5, 13, 31, 7)):
    ls1.append(j[1])
    ls3.append(j[0])
    ls4.append(j[0])


def spectral(ls1):
    plt.scatter(ls1[1:], ls1[:-1])


def count(list1, l, r):
    c = 0
    for x in list1:
        if x >= l and x <= r:
            c += 1
    return c


def chisquare(ls1, alpha=0.01, k=10):
    ls2 = []
    y = float(k)
    for i in range(k):
        ls2.append(count(ls1, (i / y), (i + 1) / y))
        # print(ls2[i])
    d = 0
    l = len(ls1)
    exp = l / k
    print(exp)
    for i in range(k):
        err = (ls2[i] - exp)**2
        d += err / exp
    stat = d
    critical = chi2.ppf(1 - alpha, k - 1)
    print(stat)
    print(critical)
    if abs(stat) >= critical:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')
# chisquare(ls1,0.05,20)


def ks_test(ls3):
    average = mean(ls3)
    print(average)
    dev = stdev(ls3)
    print(dev)
    l = len(ls3)
    for i in range(l):
        ls3[i] = (ls3[i] - average) / dev
    ls3.sort()
    normal = []
    diff = []
    for i in range(l):
        normal.append(norm.cdf(ls3[i]))
        diff.append(abs((i + 1) / l - normal[i]))
    d = max(diff)
    critical = 1.36 / sqrt(n)
    print(d)
    print(critical)
    if d >= critical:
        print('Reject H0')
    else:
        print('Fail to reject H0')


ks_test(ls3)
