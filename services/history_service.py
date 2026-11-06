"""
History Service for AGRI-MITRA
Retrieves and manages prediction history for authenticated users.
"""

from typing import List, Dict, Any, Tuple
from models.database_models import CropPrediction, FertilizerPrediction
from database.db import db


def get_user_crop_history(user_id: int, limit: int = None) -> List[CropPrediction]:
    """Returns list of crop predictions for a given user ordered newest first."""
    query = CropPrediction.query.filter_by(user_id=user_id).order_by(CropPrediction.created_at.desc())
    if limit:
        query = query.limit(limit)
    return query.all()


def get_user_fertilizer_history(user_id: int, limit: int = None) -> List[FertilizerPrediction]:
    """Returns list of fertilizer recommendations for a given user ordered newest first."""
    query = FertilizerPrediction.query.filter_by(user_id=user_id).order_by(FertilizerPrediction.created_at.desc())
    if limit:
        query = query.limit(limit)
    return query.all()


def get_user_combined_history(user_id: int) -> List[Dict[str, Any]]:
    """Returns combined and chronologically sorted list of all user predictions."""
    crops = get_user_crop_history(user_id)
    ferts = get_user_fertilizer_history(user_id)

    combined = []
    for c in crops:
        combined.append({
            'type': 'Crop Prediction',
            'category': 'crop',
            'id': c.id,
            'result': c.predicted_crop.title(),
            'detail': c.fertilizer_suggestion or 'Baseline agronomic guide',
            'created_at': c.created_at,
            'created_at_str': c.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'record': c
        })

    for f in ferts:
        combined.append({
            'type': 'Fertilizer Recommendation',
            'category': 'fertilizer',
            'id': f.id,
            'result': f.recommended_fertilizer,
            'detail': f.explanation[:80] + '...' if f.explanation and len(f.explanation) > 80 else (f.explanation or ''),
            'created_at': f.created_at,
            'created_at_str': f.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'record': f
        })

    combined.sort(key=lambda x: x['created_at'], reverse=True)
    return combined


def delete_crop_prediction(prediction_id: int, user_id: int) -> bool:
    """Deletes a crop prediction owned by the user."""
    rec = CropPrediction.query.filter_by(id=prediction_id, user_id=user_id).first()
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False


def delete_fertilizer_prediction(prediction_id: int, user_id: int) -> bool:
    """Deletes a fertilizer prediction owned by the user."""
    rec = FertilizerPrediction.query.filter_by(id=prediction_id, user_id=user_id).first()
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False
