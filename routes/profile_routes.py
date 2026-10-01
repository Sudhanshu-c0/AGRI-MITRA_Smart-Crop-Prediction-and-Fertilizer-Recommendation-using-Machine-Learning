"""
Profile Management Routes for AGRI-MITRA
Handles viewing profile, editing personal info, and changing password.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import login_required
from services.profile_service import get_profile, update_profile, change_password

profile = Blueprint('profile', __name__, url_prefix='/profile')


@profile.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    user = get_profile(user_id)
    return render_template('profile/profile.html', user=user)


@profile.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user_id = session.get('user_id')
    user = get_profile(user_id)

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        location = request.form.get('location', '').strip()

        success, msg = update_profile(
            user_id=user_id,
            full_name=full_name,
            email=email,
            phone=phone,
            location=location
        )

        if success:
            session['user_name'] = full_name
            session['user_email'] = email
            flash(msg, 'success')
            return redirect(url_for('profile.index'))
        else:
            flash(msg, 'danger')

    return render_template('profile/edit_profile.html', user=user)


@profile.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_pwd():
    user_id = session.get('user_id')

    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        success, msg = change_password(
            user_id=user_id,
            current_pwd=current_password,
            new_pwd=new_password,
            confirm_pwd=confirm_password
        )

        if success:
            flash(msg, 'success')
            return redirect(url_for('profile.index'))
        else:
            flash(msg, 'danger')

    return render_template('profile/change_password.html')
