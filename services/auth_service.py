"""
Authentication Service for AGRI-MITRA
Handles user registration, authentication, session state, and security checks.
"""

from typing import Optional, Tuple
from flask import session
from models.database_models import User
from database.db import db
from utils.validators import validate_email, validate_password_strength


def signup_user(full_name: str, email: str, password: str, phone: str = '', location: str = '') -> Tuple[bool, Optional[User], str]:
    """Registers a new user account with hashed password."""
    clean_name = (full_name or '').strip()
    clean_email = (email or '').strip().lower()

    if len(clean_name) < 2:
        return False, None, "Full name must be at least 2 characters long."
    if not validate_email(clean_email):
        return False, None, "Please provide a valid email address."
    
    is_valid_pwd, msg = validate_password_strength(password)
    if not is_valid_pwd:
        return False, None, msg

    existing = User.query.filter_by(email=clean_email).first()
    if existing:
        return False, None, "An account with this email already exists."

    user = User(
        full_name=clean_name,
        email=clean_email,
        role='user',
        phone=(phone or '').strip(),
        location=(location or '').strip()
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return True, user, "Account created successfully."


def authenticate_user(email: str, password: str) -> Tuple[bool, Optional[User], str]:
    """Authenticates a user by email and password."""
    clean_email = (email or '').strip().lower()
    user = User.query.filter_by(email=clean_email).first()

    if not user or not user.check_password(password):
        return False, None, "Invalid email or password."

    return True, user, "Authentication successful."


def login_user_session(user: User):
    """Establishes authenticated session for user."""
    session['user_id'] = user.id
    session['user_name'] = user.full_name
    session['user_email'] = user.email
    session['role'] = user.role


def logout_user_session():
    """Clears authenticated session."""
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    session.pop('role', None)


def get_current_user() -> Optional[User]:
    """Retrieves current logged-in user from database."""
    uid = session.get('user_id')
    if not uid:
        return None
    return User.query.get(uid)
