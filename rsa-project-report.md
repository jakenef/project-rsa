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

    z = mod_exp(x, floor(y/2), N)   #O(n/2) - depends on how many bits input is, halved with every call

    if (y % 2 == 0):                #O(1) - comparison and mod are constant
        return ((z * z) % N)        #O(1) - returning is constant
    else:
        return ((x * z * z) % N)    #O(1) - returning is constant
```

The largest operation is the recursive call to get z. This results in an overall time complexity of **O(n/2)**.

#### fermat

```py
def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    if N <= 1:                              #O(1) - comparison is constant
        return True                         #O(1) - returning is constant
    for i in range(k):                      #O(k) - loops k times
        a = random.randint(1, N-1)          #O(1) - generating randInt is constant
        if not (mod_exp(a, N-1, N) == 1):   #O(n/2) - mod_exp time complexity dominates constant comparisons
            return False                    #O(1) - returning is constant

    return True                             #O(1) - returning is constant
```

The largest operation is the loop k times calling mod_exp, which turns this function into a time complexity of **O(k \* n/2)**.

#### generate_large_prime

```py
def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""

    while(True):                        #O(n) - worst case, ...
        N = random.getrandbits(n_bits)  #O(1) - generating random number is constant
        if (fermat(N, 20)):             #O(n/2) - n/2 dominates k=20
            return N                    #O(1) - returning is constant
```

The largest operation is the loop n times calling fermat, which turns this function into a time complexity of **O(n^2)**.

#### Space

#### mod_exp

```py
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0:
        return 1

    z = mod_exp(x, floor(y/2), N)   #O(n/2) - call stack

    if (y % 2 == 0):
        return ((z * z) % N)
    else:
        return ((x * z * z) % N)
```

The largest space operation is the recursive call to get z. This results in an overall space complexity of **O(n/2)**.

#### fermat

```py
def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    if N <= 1:                              #O(1) - comparison is constant
        return True                         #O(1) - returning is constant
    for i in range(k):                      #O(k) - loops k times
        a = random.randint(1, N-1)          #O(1) - generating randInt is constant
        if not (mod_exp(a, N-1, N) == 1):   #O(n/2) - mod_exp time complexity dominates constant comparisons
            return False                    #O(1) - returning is constant

    return True                             #O(1) - returning is constant
```

The largest operation is the loop k times calling mod_exp, which turns this function into a time complexity of **O(k \* n/2)**.

#### generate_large_prime

```py
def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""

    while(True):                        #O(n) - worst case, ...
        N = random.getrandbits(n_bits)  #O(1) - generating random number is constant
        if (fermat(N, 20)):             #O(n/2) - n/2 dominates k=20
            return N                    #O(1) - returning is constant
```

The largest operation is the loop n times calling fermat, which turns this function into a time complexity of **O(n^2)**.

### Empirical Data

| N    | time (ms) |
| ---- | --------- |
| 64   | 0.10383   |
| 128  |           |
| 256  |           |
| 512  |           |
| 1024 |           |
| 2048 |           |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: _copy from section above_
- Measured constant of proportionality for theoretical order:
- Empirical order of growth (if different from theoretical):
- Measured constant of proportionality for empirical order:

![img](img.png)

_Fill me in_

## Core

### Design Experience

_Fill me in_

### Theoretical Analysis - Key Pair Generation

#### Time

_Fill me in_

#### Space

_Fill me in_

### Empirical Data

| N    | time (ms) |
| ---- | --------- |
| 64   |           |
| 128  |           |
| 256  |           |
| 512  |           |
| 1024 |           |
| 2048 |           |

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
