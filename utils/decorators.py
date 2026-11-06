"""
Route Protection Decorators for AGRI-MITRA
"""

from functools import wraps
from flask import session, redirect, url_for, flash, request, abort


def login_required(view_func):
    """Restricts access to authenticated users."""
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return view_func(*args, **kwargs)
    return decorated_view


def admin_required(view_func):
    """Restricts access to administrative users."""
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('Admin authentication required.', 'warning')
            return redirect(url_for('admin.login', next=request.url))
        if session.get('role') != 'admin':
            abort(403)
        return view_func(*args, **kwargs)
    return decorated_view
