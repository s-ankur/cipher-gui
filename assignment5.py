import matplotlib.pyplot as plt


def phi(n):
    result = n
    p = 2
    while(p * p <= n):
        if (n % p == 0):
            while (n % p == 0):
                n = int(n / p)
            result -= int(result / p)
        p += 1
    if (n > 1):
        result -= int(result / n)
    return result


if __name__ == "__main__":
    plt.figure("Euler Totient Function")
    n = int(input())
    plt.scatter(range(1, n + 1), list(map(phi, range(1, n + 1))), s=3, c='r')
    plt.show()
