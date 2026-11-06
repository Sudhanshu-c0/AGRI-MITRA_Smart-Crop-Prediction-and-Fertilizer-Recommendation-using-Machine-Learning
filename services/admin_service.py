"""
Admin Analytics & Management Service for AGRI-MITRA
Provides comprehensive analytics, 7-day trend computations, top crops/fertilizers,
user contact management, and audit inspection.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import func, desc
from models.database_models import User, CropPrediction, FertilizerPrediction
from database.db import db


def get_dashboard_summary() -> Dict[str, Any]:
    """Computes high-level platform usage statistics."""
    total_users = User.query.filter_by(role='user').count()
    total_crop_preds = CropPrediction.query.count()
    total_fert_preds = FertilizerPrediction.query.count()
    total_actions = total_crop_preds + total_fert_preds

    return {
        'total_users': total_users,
        'total_crop_predictions': total_crop_preds,
        'total_fertilizer_recommendations': total_fert_preds,
        'total_predictions': total_actions,
    }


def get_top_crops(limit: int = 5) -> List[Dict[str, Any]]:
    """Calculates top predicted crops with counts and percentages."""
    total = CropPrediction.query.count()
    results = (
        db.session.query(
            CropPrediction.predicted_crop,
            func.count(CropPrediction.id).label('count')
        )
        .group_by(CropPrediction.predicted_crop)
        .order_by(desc('count'))
        .limit(limit)
        .all()
    )

    top_list = []
    for crop_name, count in results:
        pct = round((count / total * 100.0), 1) if total > 0 else 0.0
        top_list.append({
            'crop': str(crop_name).title(),
            'count': int(count),
            'percentage': pct
        })
    return top_list


def get_top_fertilizers(limit: int = 5) -> List[Dict[str, Any]]:
    """Calculates top recommended fertilizers with counts and percentages."""
    total = FertilizerPrediction.query.count()
    results = (
        db.session.query(
            FertilizerPrediction.recommended_fertilizer,
            func.count(FertilizerPrediction.id).label('count')
        )
        .group_by(FertilizerPrediction.recommended_fertilizer)
        .order_by(desc('count'))
        .limit(limit)
        .all()
    )

    top_list = []
    for fert_name, count in results:
        pct = round((count / total * 100.0), 1) if total > 0 else 0.0
        top_list.append({
            'fertilizer': str(fert_name),
            'count': int(count),
            'percentage': pct
        })
    return top_list


def get_seven_day_analytics() -> Dict[str, Any]:
    """
    Computes genuine daily prediction counts for the past 7 days
    from the database using actual timestamp buckets.
    """
    today = datetime.utcnow().date()
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    labels = []
    crop_counts = []
    fert_counts = []

    for d in dates:
        day_str = d.strftime('%b %d')
        labels.append(day_str)
        
        start_dt = datetime.combine(d, datetime.min.time())
        end_dt = datetime.combine(d, datetime.max.time())

        c_cnt = CropPrediction.query.filter(
            CropPrediction.created_at >= start_dt,
            CropPrediction.created_at <= end_dt
        ).count()
        f_cnt = FertilizerPrediction.query.filter(
            FertilizerPrediction.created_at >= start_dt,
            FertilizerPrediction.created_at <= end_dt
        ).count()

        crop_counts.append(c_cnt)
        fert_counts.append(f_cnt)

    return {
        'labels': labels,
        'crop_counts': crop_counts,
        'fertilizer_counts': fert_counts,
        'total_recent_crop': sum(crop_counts),
        'total_recent_fert': sum(fert_counts)
    }


def get_all_user_predictions(search_query: Optional[str] = None, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns unified list of all predictions from all users,
    with optional keyword search and module filtering.
    """
    crop_q = CropPrediction.query
    fert_q = FertilizerPrediction.query

    records = []

    if filter_type != 'fertilizer':
        crops = crop_q.order_by(CropPrediction.created_at.desc()).all()
        for c in crops:
            u_name = c.user.full_name if c.user else 'Unknown'
            u_email = c.user.email if c.user else 'Unknown'
            # Search match
            if search_query:
                sq = search_query.lower()
                if sq not in u_name.lower() and sq not in u_email.lower() and sq not in c.predicted_crop.lower():
                    continue

            records.append({
                'type': 'Crop Prediction',
                'category': 'crop',
                'id': c.id,
                'user_id': c.user_id,
                'user_name': u_name,
                'user_email': u_email,
                'result': c.predicted_crop.title(),
                'details': f"N:{c.N} P:{c.P} K:{c.K} | Rain:{c.rainfall}mm",
                'created_at': c.created_at,
                'created_at_str': c.created_at.strftime('%Y-%m-%d %H:%M:%S') if c.created_at else ''
            })

    if filter_type != 'crop':
        ferts = fert_q.order_by(FertilizerPrediction.created_at.desc()).all()
        for f in ferts:
            u_name = f.user.full_name if f.user else 'Unknown'
            u_email = f.user.email if f.user else 'Unknown'
            if search_query:
                sq = search_query.lower()
                if sq not in u_name.lower() and sq not in u_email.lower() and sq not in f.recommended_fertilizer.lower():
                    continue

            records.append({
                'type': 'Fertilizer Recommendation',
                'category': 'fertilizer',
                'id': f.id,
                'user_id': f.user_id,
                'user_name': u_name,
                'user_email': u_email,
                'result': f.recommended_fertilizer,
                'details': f"Temp:{f.temperature}C Moisture:{f.moisture}% | Crop:{f.crop_type or 'General'}",
                'created_at': f.created_at,
                'created_at_str': f.created_at.strftime('%Y-%m-%d %H:%M:%S') if f.created_at else ''
            })

    records.sort(key=lambda x: x['created_at'] if x['created_at'] else datetime.min, reverse=True)
    return records


def get_user_contact_details(search_query: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns contact details and activity statistics for all registered users."""
    users_q = User.query.order_by(User.created_at.desc())
    if search_query:
        sq = f"%{search_query.strip()}%"
        users_q = users_q.filter(
            (User.full_name.ilike(sq)) | (User.email.ilike(sq)) | (User.phone.ilike(sq)) | (User.location.ilike(sq))
        )
    users = users_q.all()

    user_list = []
    for u in users:
        user_list.append({
            'id': u.id,
            'full_name': u.full_name,
            'email': u.email,
            'phone': u.phone or 'Not provided',
            'location': u.location or 'Not provided',
            'role': u.role,
            'crop_count': len(u.crop_predictions),
            'fertilizer_count': len(u.fertilizer_predictions),
            'total_predictions': len(u.crop_predictions) + len(u.fertilizer_predictions),
            'joined_at': u.created_at.strftime('%b %d, %Y') if u.created_at else ''
        })
    return user_list
