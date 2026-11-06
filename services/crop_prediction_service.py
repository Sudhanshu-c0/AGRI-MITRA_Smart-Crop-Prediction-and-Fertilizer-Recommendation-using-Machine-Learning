"""
Crop Prediction Service for AGRI-MITRA
Executes inference using the production Crop RandomForest model, generates basic
fertilizer suggestions, and records prediction history.
"""

from typing import Dict, Any, Tuple, Optional
from flask import current_app
import pickle
import numpy as np
import pandas as pd
from models.database_models import CropPrediction
from database.db import db
from preprocessing.data_validation import validate_crop_input
from preprocessing.feature_engineering import prepare_crop_input
from utils.helpers import get_basic_fertilizer_suggestion

_CROP_BUNDLE = None


def get_crop_model_bundle():
    """Lazily loads and caches the crop model bundle."""
    global _CROP_BUNDLE
    if _CROP_BUNDLE is None:
        model_path = current_app.config['CROP_MODEL_PATH']
        with open(model_path, 'rb') as f:
            bundle = pickle.load(f)
        _CROP_BUNDLE = bundle
    return _CROP_BUNDLE


def predict_crop(payload: Dict[str, Any], user_id: int) -> Tuple[bool, Optional[CropPrediction], Dict[str, Any], Optional[str]]:
    """
    Validates input, runs inference using Crop_Prediction_RF.pkl, generates
    basic fertilizer advice, saves record to database, and returns rich details.
    """
    is_valid, cleaned, errors = validate_crop_input(payload)
    if not is_valid:
        return False, None, {}, "; ".join(errors)

    bundle = get_crop_model_bundle()
    model = bundle['model'] if isinstance(bundle, dict) and 'model' in bundle else bundle

    # Prepare DataFrame matching exact feature names and order
    X_input = prepare_crop_input(cleaned)

    # Inference
    preds = model.predict(X_input)
    predicted_crop = str(preds[0]).strip().lower()

    # Probabilities/Confidence if supported
    confidence = None
    top_candidates = []
    if hasattr(model, 'predict_proba') and hasattr(model, 'classes_'):
        probas = model.predict_proba(X_input)[0]
        max_idx = np.argmax(probas)
        confidence = float(probas[max_idx]) * 100.0

        # Top 3 candidates
        top_indices = np.argsort(probas)[::-1][:3]
        for idx in top_indices:
            top_candidates.append({
                'crop': str(model.classes_[idx]).title(),
                'probability': round(float(probas[idx]) * 100.0, 1)
            })

    # Agronomic basic fertilizer suggestion
    fert_suggestion = get_basic_fertilizer_suggestion(predicted_crop)

    # Persist to database
    record = CropPrediction(
        user_id=user_id,
        N=cleaned['N'],
        P=cleaned['P'],
        K=cleaned['K'],
        temperature=cleaned['temperature'],
        humidity=cleaned['humidity'],
        ph=cleaned['ph'],
        rainfall=cleaned['rainfall'],
        predicted_crop=predicted_crop,
        fertilizer_suggestion=fert_suggestion
    )
    db.session.add(record)
    db.session.commit()

    result_details = {
        'id': record.id,
        'predicted_crop': predicted_crop.title(),
        'confidence': round(confidence, 1) if confidence is not None else 99.0,
        'top_candidates': top_candidates,
        'fertilizer_suggestion': fert_suggestion,
        'inputs': cleaned,
        'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    return True, record, result_details, None


def get_crop_prediction_by_id(prediction_id: int, user_id: Optional[int] = None) -> Optional[CropPrediction]:
    """Retrieves a single crop prediction with optional user ownership check."""
    query = CropPrediction.query.filter_by(id=prediction_id)
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    return query.first()
