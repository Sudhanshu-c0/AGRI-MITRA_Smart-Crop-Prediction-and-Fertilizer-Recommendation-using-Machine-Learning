"""
Crop Prediction Routes for AGRI-MITRA
Handles crop prediction form submission, ML evaluation, and result display.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from utils.decorators import login_required
from services.crop_prediction_service import predict_crop, get_crop_prediction_by_id

crop = Blueprint('crop', __name__, url_prefix='/crop')


@crop.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        user_id = session.get('user_id')
        payload = {
            'N': request.form.get('N'),
            'P': request.form.get('P'),
            'K': request.form.get('K'),
            'temperature': request.form.get('temperature'),
            'humidity': request.form.get('humidity'),
            'ph': request.form.get('ph'),
            'rainfall': request.form.get('rainfall'),
        }

        success, record, details, error_msg = predict_crop(payload, user_id=user_id)
        if success:
            flash(f"Optimal crop predicted successfully: {details['predicted_crop']}!", 'success')
            return redirect(url_for('crop.result', id=record.id))
        else:
            flash(f"Validation Error: {error_msg}", 'danger')
            return render_template('crop/crop_form.html', form_data=payload)

    # Sample baseline values to assist first-time users
    defaults = {
        'N': 90, 'P': 42, 'K': 43,
        'temperature': 20.8, 'humidity': 82.0,
        'ph': 6.5, 'rainfall': 202.9
    }
    return render_template('crop/crop_form.html', form_data=defaults)


@crop.route('/result/<int:id>')
@login_required
def result(id):
    user_id = session.get('user_id')
    # Admin can view any result, regular users only their own
    is_admin = session.get('role') == 'admin'
    prediction = get_crop_prediction_by_id(id, user_id=None if is_admin else user_id)
    if not prediction:
        abort(404)

    return render_template('crop/crop_result.html', prediction=prediction)
