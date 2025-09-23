# Project Report - RSA and Primality Tests

## Baseline

### Design Experience

On Sep. 19th, I met with Brandon Monson to discuss the design of the algorithms needed for our RSA project. We reviewed the parameters and return values for each function and how they tie into RSA. For mod_exp(x, y, N), we agreed its purpose is to compute (x^y) mod N efficiently using recursive repeated squaring, and that the return value is the reduced result of that exponentiation. For fermat(N, k) and fermat_once(N), we discussed how the input parameter N is the number to test, k is the number of trials, and the return value is a boolean indicating whether N is probably prime. We also clarified how mod_exp is used inside Fermat’s test. Finally, for generate_large_prime(n_bits), we talked about how the input specifies the bit-length of the desired prime, and the function loops until a candidate passes the Fermat test, returning a large prime suitable for RSA key generation. This discussion helped us both solidify the pseudocode into real implementations and gave us confidence about how these functions connect: mod_exp is the computational engine, Fermat uses it for primality testing, and generate_large_prime repeatedly applies Fermat to generate primes.

### Theoretical Analysis - Prime Number Generation

#### Time

#### mod_exp

```py
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0:                      #O(1) - comparison is constant
        return 1                    #O(1) - returning is constant

    z = mod_exp(x, y//2, N)         #O(n) - bit shifting means we lose one bit per shift, so this happens n times

    if (y % 2 == 0):                #O(1) - comparison and mod are constant
        return ((z * z) % N)        #O(n^2) - n^2 time complexity for multiplication
    else:
        return ((x * z * z) % N)    #O(n^2) - n^2 time complexity for multiplication
```

The largest operations are the recursive call to get z and the multiplication in the return statement. This results in an overall time complexity of **O(n^3)**.

#### fermat

```py
def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    if N <= 1:                              #O(1) - comparison is constant
        return True                         #O(1) - returning is constant
    for i in range(k):                      #O(k) - loops k times
        a = random.randint(1, N-1)          #O(<n) - definitely less than n
        if not (mod_exp(a, N-1, N) == 1):   #O(n^3) - mod_exp time complexity dominates constant comparisons
            return False                    #O(1) - returning is constant

    return True                             #O(1) - returning is constant
```

The largest operation is the loop k times calling mod_exp, which turns this function into a time complexity of **O(k \* n^3)**.

#### generate_large_prime

```py
def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""

    while(True):                        #O(n) - "on average it will halt within O(n) rounds" - Section 1.3.1, Algorithms
        N = random.getrandbits(n_bits)  #O(n) - generating random number is O(n) for bit length n
        if (fermat(N, 20)):             #O(n^3) - n^3 dominates k=20
            return N                    #O(1) - returning is constant
```

The largest operation is the loop n times calling fermat, which turns this function into a time complexity of **O(n^4)**.

#### Space

#### mod_exp

```py
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0:
        return 1

    z = mod_exp(x, y//2, N)   #O(n) - call stack and then O(n) for storing z

    if (y % 2 == 0):
        return ((z * z) % N)
    else:
        return ((x * z * z) % N)
```

We are not counting the input for the space complexity. The largest space operation is the recursive call to get z. This results in an overall space complexity of **O(n^2)**.

#### fermat

```py
def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    if N <= 1:
        return True
    for i in range(k):                      #O(k) - k small compared to N, a constant
        a = random.randint(1, N-1)          #O(n) - stores a up to N
        if not (mod_exp(a, N-1, N) == 1):   #O(n^2) - mod_exp space complexity
            return False

    return True
```

We are not counting the input for the space complexity. The largest operation is the loop k times calling mod_exp, which turns this function into a space complexity of **O(n^2)**.

#### generate_large_prime

```py
def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""

    while(True):                        #O(n) - on average, call stack is n deep (Section 1.3.1, Algorithms)
        N = random.getrandbits(n_bits)  #O(n) - generating random number is constant
        if (fermat(N, 20)):             #O(n/2) - n/2 dominates k=20
            return N                    #O(1) - returning is constant
```

We are not counting the input for space. The largest operation is the loop n times calling fermat, which turns this function into a time complexity of **O(n^2)**.

### Empirical Data

| N    | time (ms)   |
| ---- | ----------- |
| 64   | 0.82521     |
| 128  | 3.7436      |
| 256  | 26.92542    |
| 512  | 415.79199   |
| 1024 | 7792.65637  |
| 2048 | 23121.45476 |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: **O(n^4)**
- Measured constant of proportionality for theoretical order: **6.933462328106543e-09**
- Empirical order of growth (if different from theoretical): **O(n^3.7)**
- Measured constant of proportionality for empirical order: **1.0020532362591403e-07**

![generate_large_primes](generate_large_primes.png)

_Fill me in_

## Core

### Design Experience

On Sep. 19th, I met with Brandon Monson to discuss the design of generate_key_pairs(n_bits) and extended_euclid(a, b). We clarified that generate_key_pairs takes a bit length, generates two primes, computes N and φ, then selects an e coprime with φ and finds d as its modular inverse using extended_euclid. The return values are (N, e, d), which form the RSA keys. For extended_euclid, we agreed it should return coefficients (x, y, gcd) where x*a + y*b = gcd, and that y % φ provides the positive inverse for d. We also noted practical checks like avoiding p == q, using a default e if needed, and verifying correctness with sample encrypt/decrypt tests. This gave us confidence the function connects cleanly with the rest of the RSA pipeline.

### Theoretical Analysis - Key Pair Generation

#### Time

#### extended_euclid

```py
def extended_euclid(a, b) -> tuple[int, int, int]:
    if b == 0:
        return (1, 0, a)
    x, y, d = extended_euclid(b, a % b) # O(n)? how likely is b going to be 0?
    q = a // b                          # O(n^2) for division when not by 2
    return (y, x - q * y, d)            # O(n^2) for multiplication
```

The largest operations are the recursive call to get x, y, and d and the multiplication in the return statement. This results in an overall time complexity of **O(n^3)**.

#### generate_key_pairs

```py
def generate_key_pairs(n_bits) -> tuple[int, int, int]:
    """
    Generate RSA public and private key pairs.
    Randomly creates a p and q (two large n-bit primes)
    Computes N = p*q
    Computes e and d such that e*d = 1 mod (p-1)(q-1)
    Return N, e, and d
    """

    p = generate_large_prime(n_bits)            # O(n^4) as stated earlier
    q = generate_large_prime(n_bits)            # O(n^4)

    e_counter = 0

    N = p * q                                   # O(n^2)

    phi = (p - 1) * (q - 1)                     # O(n^2)
    e = primes[e_counter]

    x, y, d_gcd = extended_euclid(phi, e)       # O(n^3)

    while (d_gcd != 1):                         # O(n) whats the chance this doesn't work?
        e_counter += 1
        e = primes[e_counter]
        x, y, d_gcd = extended_euclid(phi, e)   # O(n^3)

    d = y % phi

    return (N, e, d)
```

The largest operations are the calls to generate large primes and to get x, y, and d_gcd in the while loop. This results in an overall time complexity of **O(n^4)**.

#### Space

_Fill me in_

### Empirical Data

| N    | time (ms)  |
| ---- | ---------- |
| 64   | 2.15869    |
| 128  | 9.20548    |
| 256  | 76.91126   |
| 512  | 1145.24369 |
| 1024 | 8262.48736 |
| 2048 |            |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: _copy from section above_
- Measured constant of proportionality for theoretical order:
- Empirical order of growth (if different from theoretical):
- Measured constant of proportionality for empirical order:

![img](img.png)

_Fill me in_

## Stretch 1

### Design Experience

_Fill me in_

### Theoretical Analysis - Encrypt and Decrypt

#### Time

_Fill me in_

#### Space

_Fill me in_

### Empirical Data

#### Encryption

| N    | time (ms) |
| ---- | --------- |
| 64   |           |
| 128  |           |
| 256  |           |
| 512  |           |
| 1024 |           |
| 2048 |           |

#### Decryption

| N    | time (ms) |
| ---- | --------- |
| 64   |           |
| 128  |           |
| 256  |           |
| 512  |           |
| 1024 |           |
| 2048 |           |

### Comparison of Theoretical and Empirical Results

#### Encryption

- Theoretical order of growth: _copy from section above_
- Measured constant of proportionality for theoretical order:
- Empirical order of growth (if different from theoretical):
- Measured constant of proportionality for empirical order:

![img](img.png)

_Fill me in_

#### Decryption

- Theoretical order of growth: _copy from section above_
- Measured constant of proportionality for theoretical order:
- Empirical order of growth (if different from theoretical):
- Measured constant of proportionality for empirical order:

![img](img.png)

_Fill me in_

### Encrypting and Decrypting With A Classmate

_Fill me in_

## Stretch 2

### Design Experience

_Fill me in_

### Discussion: Probabilistic Natures of Fermat and Miller Rabin

_Fill me in_

## Project Review

_Fill me in_
