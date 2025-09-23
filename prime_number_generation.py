from math import floor
import sys
from time import time
import random
sys.setrecursionlimit(4000)


# You will need to implement this function and change the return value.
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0:
        return 1
    
    z = mod_exp(x, (y//2), N)

    if (y % 2 == 0):
        return ((z * z) % N)
    else:
        return ((x * z * z) % N)


def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    if N <= 1:
        return True
    for i in range(k):
        a = random.randint(1, N-1)
        if not (mod_exp(a, N-1, N) == 1):
            return False
        
    return True

def miller_rabin(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    return False


def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""

    while(True):
        N = random.getrandbits(n_bits)
        if (fermat(N, 20)):
            return N

def main(n_bits: int):
    start = time()
    large_prime = generate_large_prime(n_bits)
    print(large_prime)
    print(f'Generation took {time() - start} seconds')


if __name__ == '__main__':
    main(int(sys.argv[1]))
