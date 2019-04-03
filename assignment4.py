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

def lcg(initial = 0, constants =[34,8], m=500 ):
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

def bbs(initial =101, constants =  [71,503]):
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

def count(numbers, n, r):
	ctr = 0
	for x in numbers:
		if x >= n and x <= r: ctr += 1
	return ctr


def chisquare(numbers, alpha=0.05, k=10):
	counts = []
	for i in range(k):
		counts.append(count(numbers, (i / k), (i + 1) /k))
	difference, n = 0, len(numbers)
	expected = n / k
	for i in range(k):
		err = (counts[i] - expected)**2
		difference += err / expected
	return abs(difference) >= chi2.ppf(1 - alpha, k - 1)
		

def ks_test(numbers):
	average = mean(numbers)
	deviation = stdev(numbers)
	n = len(numbers)
	for i in range(n):
		numbers[i] = (numbers[i] - average) / deviation
	numbers.sort()
	normal = []
	difference = []
	for i in range(n):
		normal.append(norm.cdf(numbers[i]))
		difference.append(abs((i + 1) / n - normal[i]))
	max_difference = max(difference)
	critical = 1.36 / sqrt(n)
	return max_difference >= critical


if __name__ == "__main__":
	n =1000
	prngs ,tests = ('lcg', 'bbs', 'ansi'), ('spectral', 'chisquare', 'ks_test')
	for prng in prngs:
		numbers = list(islice(vars()[prng](),n))
		for test in tests:
			print(test,'on',prng,vars()[test](numbers))



	
