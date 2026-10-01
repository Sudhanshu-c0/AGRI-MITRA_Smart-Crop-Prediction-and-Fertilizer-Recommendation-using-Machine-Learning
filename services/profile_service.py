"""
Profile Service for AGRI-MITRA
Handles user profile updates, password modifications, and account security.
"""

from typing import Tuple, Optional
from models.database_models import User
from database.db import db
from utils.validators import validate_email, validate_password_strength


def get_profile(user_id: int) -> Optional[User]:
    """Retrieves user profile by ID."""
    return User.query.get(user_id)


def update_profile(user_id: int, full_name: str, email: str, phone: str = '', location: str = '') -> Tuple[bool, str]:
    """Updates user personal details with email uniqueness check."""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found."

    clean_name = (full_name or '').strip()
    clean_email = (email or '').strip().lower()

    if len(clean_name) < 2:
        return False, "Full name must be at least 2 characters long."
    if not validate_email(clean_email):
        return False, "Please provide a valid email address."

    # Check email duplicate across other users
    existing = User.query.filter(User.email == clean_email, User.id != user_id).first()
    if existing:
        return False, "This email is already in use by another account."

    user.full_name = clean_name
    user.email = clean_email
    user.phone = (phone or '').strip()
    user.location = (location or '').strip()

    db.session.commit()
    return True, "Profile updated successfully."


def change_password(user_id: int, current_pwd: str, new_pwd: str, confirm_pwd: str) -> Tuple[bool, str]:
    """Changes user password with verification of current password."""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found."

    if not user.check_password(current_pwd):
        return False, "Current password is incorrect."

    if new_pwd != confirm_pwd:
        return False, "New passwords do not match."

    is_valid, msg = validate_password_strength(new_pwd)
    if not is_valid:
        return False, msg

    user.set_password(new_pwd)
    db.session.commit()
    return True, "Password changed successfully."
