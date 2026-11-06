"""
Security and Hashing Utilities for AGRI-MITRA
"""

import secrets
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """Generates secure scrypt or pbkdf2 hash for user password."""
    return generate_password_hash(password)


def verify_password(hashed: str, password: str) -> bool:
    """Verifies plain password against hash."""
    return check_password_hash(hashed, password)


def generate_token(length: int = 32) -> str:
    """Generates a secure random hex token."""
    return secrets.token_hex(length // 2)
