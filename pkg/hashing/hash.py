"""
This file contains functions to handle hashing operations such as generating
hashes for files and strings. These functions can be used to generate unique
hashes for data, compare hashes, and verify data integrity.
"""

import hashlib


def make_hash(data: str) -> str:
    """
    make_hash
    This function generates a hash for the given data using the SHA-256 algorithm.

    Args:
        data (str): The input data for which the hash needs to be generated.

    Returns:
        str: The hash value generated for the input data.
    """

    hash_object = hashlib.sha1(data.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


print("Hello, World!".encode(), make_hash("Hello, World!"))
