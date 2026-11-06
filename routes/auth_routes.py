"""
Authentication Routes for AGRI-MITRA
Handles Sign Up, Log In, and Log Out for standard platform users.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import signup_user, authenticate_user, login_user_session, logout_user_session

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session and session.get('role') != 'admin':
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        location = request.form.get('location', '').strip()

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/signup.html', full_name=full_name, email=email, phone=phone, location=location)

        success, user, message = signup_user(
            full_name=full_name,
            email=email,
            password=password,
            phone=phone,
            location=location
        )

        if success:
            flash('Registration successful! Please log in with your credentials.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
            return render_template('auth/signup.html', full_name=full_name, email=email, phone=phone, location=location)

    return render_template('auth/signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session and session.get('role') != 'admin':
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        success, user, message = authenticate_user(email, password)
        if success:
            login_user_session(user)
            flash(f"Welcome back, {user.full_name}!", 'success')
            next_url = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_url or url_for('admin.dashboard'))
            return redirect(next_url or url_for('dashboard.index'))
        else:
            flash(message, 'danger')
            return render_template('auth/login.html', email=email)

    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    logout_user_session()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('home.index'))
