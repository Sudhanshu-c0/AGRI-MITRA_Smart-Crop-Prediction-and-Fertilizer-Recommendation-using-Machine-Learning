"""
Admin Management & Analytics Routes for AGRI-MITRA
Provides comprehensive administrator dashboard, 7-day analytics, top crops/fertilizers,
user prediction inspection, and user contact management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from utils.decorators import admin_required
from services.auth_service import authenticate_user, login_user_session, logout_user_session
from services.admin_service import (
    get_dashboard_summary,
    get_top_crops,
    get_top_fertilizers,
    get_seven_day_analytics,
    get_all_user_predictions,
    get_user_contact_details
)
from models.database_models import User
from database.db import db

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('role') == 'admin':
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        success, user, message = authenticate_user(email, password)
        if success and user.role == 'admin':
            login_user_session(user)
            flash('Admin authentication successful.', 'success')
            return redirect(url_for('admin.dashboard'))
        elif success and user.role != 'admin':
            flash('Access denied: Administrator privileges required.', 'danger')
        else:
            flash('Invalid administrator credentials.', 'danger')

    return render_template('admin/admin_login.html')


@admin.route('/logout')
def logout():
    logout_user_session()
    flash('Admin signed out.', 'info')
    return redirect(url_for('admin.login'))


@admin.route('/dashboard')
@admin_required
def dashboard():
    summary = get_dashboard_summary()
    top_c = get_top_crops(limit=5)
    top_f = get_top_fertilizers(limit=5)
    analytics_7d = get_seven_day_analytics()
    recent_predictions = get_all_user_predictions()[:10]

    return render_template(
        'admin/admin_dashboard.html',
        summary=summary,
        top_crops=top_c,
        top_fertilizers=top_f,
        analytics=analytics_7d,
        recent_predictions=recent_predictions
    )


@admin.route('/top-crops')
@admin_required
def top_crops():
    top_c = get_top_crops(limit=10)
    return render_template('admin/top_crops.html', top_crops=top_c)


@admin.route('/top-fertilizers')
@admin_required
def top_fertilizers():
    top_f = get_top_fertilizers(limit=10)
    return render_template('admin/top_fertilizers.html', top_fertilizers=top_f)


@admin.route('/predictions')
@admin_required
def predictions():
    query = request.args.get('q', '').strip()
    filter_type = request.args.get('type', 'all')
    all_preds = get_all_user_predictions(search_query=query, filter_type=filter_type)
    return render_template('admin/user_predictions.html', predictions=all_preds, query=query, filter_type=filter_type)


@admin.route('/users')
@admin_required
def users():
    query = request.args.get('q', '').strip()
    user_list = get_user_contact_details(search_query=query)
    return render_template('admin/user_details.html', users=user_list, query=query)


@admin.route('/user/<int:user_id>')
@admin_required
def user_detail(user_id):
    u = User.query.get_or_404(user_id)
    return render_template(
        'admin/prediction_table.html',
        target_user=u,
        crop_predictions=u.crop_predictions,
        fertilizer_predictions=u.fertilizer_predictions
    )
