from passlib.context import CryptContext

# CryptContext is our hashing settings object.
# We tell it to use bcrypt as the hashing algorithm.
# Bcrypt is intentionally slow, making brute force attacks harder.
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(plain_password: str) -> str:
    # Takes a plain text password from signup
    # Returns a bcrypt hashed version to store in the database
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Used during login - not signup
    # Compares the plain password the user typed 
    # against the hash we have stored in the database
    # Returns True if they match, False otherwise
    return pwd_context.verify(plain_password, hashed_password)