"""
CSV Export Service for AGRI-MITRA
Generates streaming CSV responses for user histories and administrative audits.
"""

import io
import csv
from typing import List, Optional
from flask import Response
from models.database_models import User, CropPrediction, FertilizerPrediction


def export_crop_predictions_csv(user_id: Optional[int] = None) -> Response:
    """Exports crop prediction records to CSV."""
    query = CropPrediction.query
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    records = query.order_by(CropPrediction.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Headers
    headers = [
        'Prediction ID', 'User ID', 'User Name', 'User Email',
        'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)',
        'Temperature (C)', 'Humidity (%)', 'Soil pH', 'Rainfall (mm)',
        'Predicted Crop', 'Fertilizer Suggestion', 'Created At'
    ]
    writer.writerow(headers)

    for r in records:
        writer.writerow([
            r.id,
            r.user_id,
            r.user.full_name if r.user else 'Unknown',
            r.user.email if r.user else 'Unknown',
            r.N,
            r.P,
            r.K,
            r.temperature,
            r.humidity,
            r.ph,
            r.rainfall,
            r.predicted_crop.title(),
            r.fertilizer_suggestion or '',
            r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
        ])

    filename = f"crop_predictions_{'user' if user_id else 'all'}.csv"
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


def export_fertilizer_predictions_csv(user_id: Optional[int] = None) -> Response:
    """Exports fertilizer recommendation records to CSV."""
    query = FertilizerPrediction.query
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    records = query.order_by(FertilizerPrediction.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    headers = [
        'Recommendation ID', 'User ID', 'User Name', 'User Email',
        'Temperature (C)', 'Humidity (%)', 'Soil Moisture (%)',
        'Soil Type', 'Crop Type', 'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)',
        'Recommended Fertilizer', 'Scientific Rationale', 'Created At'
    ]
    writer.writerow(headers)

    for r in records:
        writer.writerow([
            r.id,
            r.user_id,
            r.user.full_name if r.user else 'Unknown',
            r.user.email if r.user else 'Unknown',
            r.temperature,
            r.humidity,
            r.moisture,
            r.soil_type or '',
            r.crop_type or '',
            r.N,
            r.P,
            r.K,
            r.recommended_fertilizer,
            r.explanation or '',
            r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
        ])

    filename = f"fertilizer_recommendations_{'user' if user_id else 'all'}.csv"
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


def export_combined_history_csv(user_id: Optional[int] = None) -> Response:
    """Exports unified prediction history (crops + fertilizers) to CSV."""
    crop_query = CropPrediction.query
    fert_query = FertilizerPrediction.query
    if user_id is not None:
        crop_query = crop_query.filter_by(user_id=user_id)
        fert_query = fert_query.filter_by(user_id=user_id)

    crops = crop_query.all()
    ferts = fert_query.all()

    items = []
    for c in crops:
        items.append({
            'module': 'Crop Prediction',
            'id': c.id,
            'user_name': c.user.full_name if c.user else 'Unknown',
            'user_email': c.user.email if c.user else 'Unknown',
            'result': c.predicted_crop.title(),
            'advisory': c.fertilizer_suggestion or '',
            'created_at': c.created_at
        })
    for f in ferts:
        items.append({
            'module': 'Fertilizer Recommendation',
            'id': f.id,
            'user_name': f.user.full_name if f.user else 'Unknown',
            'user_email': f.user.email if f.user else 'Unknown',
            'result': f.recommended_fertilizer,
            'advisory': f.explanation or '',
            'created_at': f.created_at
        })

    items.sort(key=lambda x: x['created_at'] if x['created_at'] else datetime.min, reverse=True)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Record Type', 'ID', 'User Name', 'User Email', 'Model Result', 'Advisory / Explanation', 'Timestamp'])

    for it in items:
        writer.writerow([
            it['module'],
            it['id'],
            it['user_name'],
            it['user_email'],
            it['result'],
            it['advisory'],
            it['created_at'].strftime('%Y-%m-%d %H:%M:%S') if it['created_at'] else ''
        ])

    filename = f"agri_mitra_history_{'user' if user_id else 'all'}.csv"
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


def export_users_csv() -> Response:
    """Exports all registered users and contact details to CSV (admin audit)."""
    users = User.query.order_by(User.created_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['User ID', 'Full Name', 'Email', 'Phone', 'Location', 'Role', 'Crop Predictions Count', 'Fertilizer Recs Count', 'Registered Date'])
    for u in users:
        writer.writerow([
            u.id,
            u.full_name,
            u.email,
            u.phone or 'Not Provided',
            u.location or 'Not Provided',
            u.role,
            len(u.crop_predictions),
            len(u.fertilizer_predictions),
            u.created_at.strftime('%Y-%m-%d %H:%M:%S') if u.created_at else ''
        ])

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=agri_mitra_users_audit.csv'}
    )
