from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from app.config import JWT_SECRET
import secrets
from fastapi import HTTPException
from app.services.database import supabase


# Bcrypt is intentionally slow (cost factor ~12 rounds by default), making
# offline brute-force attacks expensive even if the database is leaked.
# Faster algorithms like MD5 or SHA-256 are unsuitable for passwords.
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
    # We embed company_id in the token payload so that protected routes never
    # accept company_id as a user-supplied parameter. This prevents one company
    # from impersonating another by simply passing a different ID in the request.
    # 7-day expiry balances security (short-lived tokens) with UX (not logging
    # out active users every few hours).
    payload = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(days=7)
    payload["exp"] = expiry
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token


def decode_access_token(token):
    # Returns None instead of raising so callers can decide how to handle
    # invalid tokens (e.g. raise HTTP 401 vs redirect to login).
    try:
        access_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return access_token
    except JWTError:
        return None


def generate_api_key():
    # API keys don't need bcrypt hashing because they are long, high-entropy
    # random strings (128 bits via token_hex). Unlike passwords, they can't be
    # brute-forced, so the bcrypt cost factor would just add latency with no
    # security benefit. We store them in plaintext so we can display them back
    # to the company owner.
    # The "vrl_" prefix makes keys identifiable as Virlo keys, which helps
    # companies spot them in environment variables and security audits.
    api_key = "vrl_" + secrets.token_hex(16)
    return api_key


def get_company_id_from_token(authorization):
    # We raise HTTPException instead of returning an error dict because FastAPI
    # only sets a non-200 status code when an exception is raised. Returning a
    # plain dict always produces a 200 OK, which would silently pass auth
    # failures to the client as successes.
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Strip "Bearer " prefix to get the raw JWT token
    token = authorization.replace("Bearer ", "")

    # Decode and validate the token — returns None if invalid or expired
    decoded_access_token = decode_access_token(token)

    if decoded_access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # company_id was embedded at token creation time, so this is the verified
    # identity of whoever owns this token — not a value the caller can forge.
    company_id = decoded_access_token["company_id"]

    return company_id

def get_company_id_from_api_key(authorization):
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    api_key =  authorization

    response = (
        supabase.table("companies")
        .select("api_key, id") #table name 
        .eq("api_key", api_key)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return response.data[0]["id"]






