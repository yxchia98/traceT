import numpy as np
from random import seed
from random import choice
import time


class RSA:
    # public key e, n
    def encrypt(self, val):
        return pow(val, self.e) % self.n

    # private key d, n
    def decrypt(self, val):
        m = pow((val % self.n), self.d) % self.n
        return m

    def __init__(self):
        # p and q must be primes
        self.p = 773
        self.q = 2371
        self.n = self.p * self.q

        phi = (self.p-1)*(self.q-1)

        # 2 < e < phi
        # using fermat number
        self.e = 65537

        self.d = modInverse(self.e, phi)


def gcd(a, b):
    temp = a % b
    while temp:
        a = b
        b = temp
        temp = a % b


def modInverse(a, m):
    for x in range(1, m):
        if (((a % m) * (x % m)) % m == 1):
            return x
    return -1


# driver code
# rsa = RSA()
# #print('private key', rsa.d)
# num = int(input("Enter a number to encrypt:"))
# start = time.time()
# en = rsa.encrypt(num)
# print('encrypted:', en)
# print('decrypted:', rsa.decrypt(en))
# print(time.time() - start)
