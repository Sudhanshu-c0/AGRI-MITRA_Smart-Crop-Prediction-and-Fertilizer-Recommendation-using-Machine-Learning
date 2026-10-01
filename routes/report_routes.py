"""
Report Routes for AGRI-MITRA
Serves downloadable PDF reports and HTML report view summaries.
"""

from flask import Blueprint, render_template, Response, abort, session
from utils.decorators import login_required
from services.crop_prediction_service import get_crop_prediction_by_id
from services.fertilizer_recommendation_service import get_fertilizer_prediction_by_id
from services.report_service import generate_crop_report_pdf, generate_fertilizer_report_pdf
from services.auth_service import get_current_user

report = Blueprint('report', __name__, url_prefix='/reports')


@report.route('/crop/<int:id>/pdf')
@login_required
def download_crop_pdf(id):
    user_id = session.get('user_id')
    is_admin = session.get('role') == 'admin'
    prediction = get_crop_prediction_by_id(id, user_id=None if is_admin else user_id)
    if not prediction:
        abort(404)

    pdf_bytes = generate_crop_report_pdf(prediction, prediction.user)
    filename = f"AGRI_MITRA_Crop_Report_CP{prediction.id:04d}.pdf"

    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )


@report.route('/fertilizer/<int:id>/pdf')
@login_required
def download_fertilizer_pdf(id):
    user_id = session.get('user_id')
    is_admin = session.get('role') == 'admin'
    prediction = get_fertilizer_prediction_by_id(id, user_id=None if is_admin else user_id)
    if not prediction:
        abort(404)

    pdf_bytes = generate_fertilizer_report_pdf(prediction, prediction.user)
    filename = f"AGRI_MITRA_Fertilizer_Report_FR{prediction.id:04d}.pdf"

    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )


@report.route('/crop/<int:id>/view')
@login_required
def view_crop_report(id):
    user_id = session.get('user_id')
    is_admin = session.get('role') == 'admin'
    prediction = get_crop_prediction_by_id(id, user_id=None if is_admin else user_id)
    if not prediction:
        abort(404)

    return render_template('reports/crop_report.html', prediction=prediction)


@report.route('/fertilizer/<int:id>/view')
@login_required
def view_fertilizer_report(id):
    user_id = session.get('user_id')
    is_admin = session.get('role') == 'admin'
    prediction = get_fertilizer_prediction_by_id(id, user_id=None if is_admin else user_id)
    if not prediction:
        abort(404)

    return render_template('reports/fertilizer_report.html', prediction=prediction)
