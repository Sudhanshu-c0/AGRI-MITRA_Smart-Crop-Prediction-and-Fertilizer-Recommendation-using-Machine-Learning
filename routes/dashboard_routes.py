"""
User Dashboard Routes for AGRI-MITRA
Provides personal summary metrics, quick actions, and recent activity.
"""

from flask import Blueprint, render_template, session
from utils.decorators import login_required
from services.history_service import get_user_crop_history, get_user_fertilizer_history, get_user_combined_history
from services.auth_service import get_current_user

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@login_required
def index():
    user = get_current_user()
    user_id = session.get('user_id')

    crops = get_user_crop_history(user_id)
    ferts = get_user_fertilizer_history(user_id)
    recent_activity = get_user_combined_history(user_id)[:6]

    metrics = {
        'total_crop_predictions': len(crops),
        'total_fertilizer_recommendations': len(ferts),
        'total_actions': len(crops) + len(ferts),
        'latest_crop': crops[0].predicted_crop.title() if crops else 'None yet',
        'latest_fertilizer': ferts[0].recommended_fertilizer if ferts else 'None yet'
    }

    return render_template(
        'dashboard/dashboard.html',
        user=user,
        metrics=metrics,
        recent_activity=recent_activity
    )
