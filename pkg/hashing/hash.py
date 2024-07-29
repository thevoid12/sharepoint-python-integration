"""
This file contains functions to handle hashing operations such as generating
hashes for files and strings. These functions can be used to generate unique
hashes for data, compare hashes, and verify data integrity.
"""

import hashlib


def make_hash(data: bytes | str) -> str:
    """
    Generates a SHA-256 hash of the given data. The data can be a string or bytes.

    Args:
        data (str or bytes): The data to hash.

    Returns:
        str: The hexadecimal digest of the hash.
    """
    try:
        # Check if the data is bytes
        if isinstance(data, bytes):
            # If the data is bytes, use it as is
            pass
        elif isinstance(data, str):
            # If the data is a string, encode it to bytes
            data = data.encode("utf-8")
        else:
            # If the data is neither bytes nor a string, raise an error
            raise ValueError("Data must be bytes or a string")

        # Create a SHA-256 hash object
        hash_obj = hashlib.sha256()
        # Update the hash object with the data
        hash_obj.update(data)
        # Return the hexadecimal digest of the hash
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Error occurred: {e}")
        raise


if __name__ == "__main__":
    print("Hello, World!".encode(), make_hash("Hello, World!"))
