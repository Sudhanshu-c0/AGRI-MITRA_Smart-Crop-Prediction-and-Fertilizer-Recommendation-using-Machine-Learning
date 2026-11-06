"""
CSV Export Routes for AGRI-MITRA
Allows users and administrators to export history data to standard CSV files.
"""

from flask import Blueprint, session, abort
from utils.decorators import login_required, admin_required
from services.csv_export_service import (
    export_crop_predictions_csv,
    export_fertilizer_predictions_csv,
    export_combined_history_csv,
    export_users_csv
)

export = Blueprint('export', __name__, url_prefix='/export')


@export.route('/crop/csv')
@login_required
def export_user_crop_csv():
    user_id = session.get('user_id')
    return export_crop_predictions_csv(user_id=user_id)


@export.route('/fertilizer/csv')
@login_required
def export_user_fertilizer_csv():
    user_id = session.get('user_id')
    return export_fertilizer_predictions_csv(user_id=user_id)


@export.route('/history/csv')
@login_required
def export_user_history_csv():
    user_id = session.get('user_id')
    return export_combined_history_csv(user_id=user_id)


@export.route('/admin/all-predictions/csv')
@admin_required
def export_admin_all_predictions_csv():
    return export_combined_history_csv(user_id=None)


@export.route('/admin/users/csv')
@admin_required
def export_admin_users_csv():
    return export_users_csv()
