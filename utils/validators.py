"""
Input Validators for AGRI-MITRA
"""

import re
from typing import Tuple, List, Dict, Any


def validate_email(email: str) -> bool:
    """Validates email format using regex."""
    if not email or not isinstance(email, str):
        return False
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(regex, email.strip()))


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Ensures password meets security criteria."""
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def validate_user_registration(name: str, email: str, password: str, confirm_password: str) -> Tuple[bool, List[str]]:
    """Validates user signup form fields."""
    errors = []
    if not name or len(name.strip()) < 2:
        errors.append("Full name must be at least 2 characters long.")
    if not validate_email(email):
        errors.append("Please enter a valid email address.")
    if password != confirm_password:
        errors.append("Passwords do not match.")
    is_strong, msg = validate_password_strength(password)
    if not is_strong:
        errors.append(msg)
    return len(errors) == 0, errors
