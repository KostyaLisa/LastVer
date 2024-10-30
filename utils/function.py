import hashlib

def hesh_password(password):
    """
    Hashes the password using SHA-256 algorithm.
    """
    # Convert the password to bytes and hash it
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password