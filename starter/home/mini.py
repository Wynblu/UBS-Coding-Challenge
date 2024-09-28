import sys


def mini_hash(data):
    """
    A simple hash function for binary data, producing a 20-bit hash.

    Parameters:
    - data: Input binary data to hash.

    Returns:
    - A hash value as a 5-character hexadecimal string.
    """
    hash_value = 0
    for byte in data:
        hash_value = (hash_value * 31 + byte) % (2**20)

    # Convert the hash value to a 4-character hexadecimal string
    return f"{hash_value:05x}"


def hash_file(file_path):
    """
    Hash the contents of a file in binary mode and return a hexadecimal string.

    Parameters:
    - file_path: Path to the file to hash.

    Returns:
    - A hash value as a 4-character hexadecimal string.
    """
    try:
        with open(file_path, "rb") as file:
            content = file.read()
            return mini_hash(content)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path1> <file_path2> ...")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        hash_value = hash_file(file_path)
        if hash_value is not None:
            print(f"mini ({file_path}) = {hash_value}")
