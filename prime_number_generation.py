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
    if N <= 1:
        return False
    if N <= 3:
        return True              # 2,3 are prime
    if N % 2 == 0:
        return False 
    t = 0
    u = N - 1
    while (u % 2 == 0):
        u = u // 2
        t = t + 1
    
    for i in range(k):
        a = random.randint(2, N-2)
        x = mod_exp(a, u, N)

        if x == 1 or x == N-1:
            continue
        
        found = False

        for j in range(t-1):
            x = (x * x) % N
            if x == N-1:
                found = True
                break
        
        if not found:
            return False
        
    return True


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
