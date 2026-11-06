"""
History Routes for AGRI-MITRA
Allows users to browse and filter their past crop predictions and fertilizer recommendations.
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from utils.decorators import login_required
from services.history_service import (
    get_user_crop_history, get_user_fertilizer_history,
    get_user_combined_history, delete_crop_prediction, delete_fertilizer_prediction
)

history = Blueprint('history', __name__, url_prefix='/history')


@history.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    combined = get_user_combined_history(user_id)
    return render_template('history/history.html', history_items=combined)


@history.route('/crop')
@login_required
def crop_history():
    user_id = session.get('user_id')
    crops = get_user_crop_history(user_id)
    return render_template('history/crop_history.html', crops=crops)


@history.route('/fertilizer')
@login_required
def fertilizer_history():
    user_id = session.get('user_id')
    ferts = get_user_fertilizer_history(user_id)
    return render_template('history/fertilizer_history.html', fertilizers=ferts)


@history.route('/delete/crop/<int:id>', methods=['POST'])
@login_required
def delete_crop(id):
    user_id = session.get('user_id')
    if delete_crop_prediction(id, user_id):
        flash('Crop prediction record deleted successfully.', 'info')
    else:
        flash('Could not delete record.', 'danger')
    return redirect(request.referrer or url_for('history.crop_history'))


@history.route('/delete/fertilizer/<int:id>', methods=['POST'])
@login_required
def delete_fertilizer(id):
    user_id = session.get('user_id')
    if delete_fertilizer_prediction(id, user_id):
        flash('Fertilizer recommendation record deleted successfully.', 'info')
    else:
        flash('Could not delete record.', 'danger')
    return redirect(request.referrer or url_for('history.fertilizer_history'))
