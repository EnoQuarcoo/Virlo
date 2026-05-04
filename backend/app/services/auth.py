from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from app.config import JWT_SECRET



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

def create_access_token(data: dict):
    payload = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(days=7)
    payload["exp"] = expiry
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token


def decode_access_token(token):
    try: 
        access_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return access_token
    except JWTError:
        return None
    



