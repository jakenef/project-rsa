import sys
from pathlib import Path
from time import time
from typing import Iterable

from prime_number_generation import mod_exp

sys.setrecursionlimit(5000)


def stream_chunks(message: bytes, n_bytes: int) -> Iterable[int]:
    """
    Read the message N bits at a time, returning a sequence of integers
    """
    # First, pad the beginning with zeros so the length of the message is
    #  a multiple of n_bytes
    needed_zeros = n_bytes - (len(message) % n_bytes)
    message = b'\x00' * needed_zeros + message

    for chunk_number in range((len(message) // n_bytes)):
        start = chunk_number * n_bytes
        yield int.from_bytes(message[start:start + n_bytes], byteorder='big')


def to_bytes(integer: int, n_bytes: int) -> bytes:
    return integer.to_bytes(n_bytes, 'big')


def read_key(key_file: Path) -> tuple[int, int, int]:
    N, exponent = key_file.read_text().splitlines()
    N = int(N)
    exponent = int(exponent)
    n_bytes = (N.bit_length() + 7) // 8
    return n_bytes, N, exponent


def main(key_file: Path, message_file: Path, output_file: Path):
    """
    Encrypt or decrypt `message_file` and write the result in `output_file`
    """

    n_bytes, N, exponent = read_key(key_file)

    input_bytes = message_file.read_bytes()

    start = time()

    result = []
    for chunk in stream_chunks(input_bytes, n_bytes):
        encrypted_chunk = mod_exp(chunk, exponent, N)
        encrypted_bytes = to_bytes(encrypted_chunk, n_bytes)
        result.append(encrypted_bytes)

    print(f'{time() - start} seconds elapsed')

    output_file.write_bytes(b''.join(result).rstrip(b'\x00'))


if __name__ == '__main__':
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
