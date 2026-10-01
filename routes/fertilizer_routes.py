"""
Fertilizer Recommendation Routes for AGRI-MITRA
Handles fertilizer recommendation form submission, ML inference, and result display.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from utils.decorators import login_required
from services.fertilizer_recommendation_service import predict_fertilizer, get_fertilizer_prediction_by_id

fertilizer = Blueprint('fertilizer', __name__, url_prefix='/fertilizer')


@fertilizer.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    if request.method == 'POST':
        user_id = session.get('user_id')
        payload = {
            'temperature': request.form.get('temperature'),
            'humidity': request.form.get('humidity'),
            'Moisture': request.form.get('Moisture') or request.form.get('moisture'),
            'soil_type': request.form.get('soil_type'),
            'crop_type': request.form.get('crop_type'),
            'N': request.form.get('N'),
            'P': request.form.get('P'),
            'K': request.form.get('K'),
        }

        success, record, details, error_msg = predict_fertilizer(payload, user_id=user_id)
        if success:
            flash(f"Prescribed fertilizer: {details['recommended_fertilizer']}!", 'success')
            return redirect(url_for('fertilizer.result', id=record.id))
        else:
            flash(f"Validation Error: {error_msg}", 'danger')
            return render_template('fertilizer/fertilizer_form.html', form_data=payload)

    defaults = {
        'temperature': 26, 'humidity': 52, 'Moisture': 38,
        'soil_type': 'Sandy', 'crop_type': 'Maize',
        'N': 37, 'P': 0, 'K': 0
    }
    return render_template('fertilizer/fertilizer_form.html', form_data=defaults)


@fertilizer.route('/result/<int:id>')
@login_required
def result(id):
    user_id = session.get('user_id')
    is_admin = session.get('role') == 'admin'
    prediction = get_fertilizer_prediction_by_id(id, user_id=None if is_admin else user_id)
    if not prediction:
        abort(404)

    return render_template('fertilizer/fertilizer_result.html', prediction=prediction)
