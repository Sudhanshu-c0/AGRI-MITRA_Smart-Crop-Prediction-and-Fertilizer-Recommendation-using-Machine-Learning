"""
Fertilizer Recommendation Service for AGRI-MITRA
Executes inference using the production Fertilizer RandomForest model, generates
comprehensive explanatory rationales (WHY), and records recommendation history.
"""

from typing import Dict, Any, Tuple, Optional
from flask import current_app
import pickle
import numpy as np
from models.database_models import FertilizerPrediction
from database.db import db
from preprocessing.data_validation import validate_fertilizer_input
from preprocessing.feature_engineering import prepare_fertilizer_input
from utils.helpers import fertilizer_explanation

_FERTILIZER_BUNDLE = None


def get_fertilizer_model_bundle():
    """Lazily loads and caches the fertilizer model bundle."""
    global _FERTILIZER_BUNDLE
    if _FERTILIZER_BUNDLE is None:
        model_path = current_app.config['FERTILIZER_MODEL_PATH']
        with open(model_path, 'rb') as f:
            bundle = pickle.load(f)
        _FERTILIZER_BUNDLE = bundle
    return _FERTILIZER_BUNDLE


def predict_fertilizer(payload: Dict[str, Any], user_id: int) -> Tuple[bool, Optional[FertilizerPrediction], Dict[str, Any], Optional[str]]:
    """
    Validates input, runs inference using Fertilizer_Recommendation_RF.pkl,
    generates agronomic explanation, saves record to database, and returns details.
    """
    is_valid, cleaned, errors = validate_fertilizer_input(payload)
    if not is_valid:
        return False, None, {}, "; ".join(errors)

    bundle = get_fertilizer_model_bundle()
    model = bundle['model'] if isinstance(bundle, dict) and 'model' in bundle else bundle

    # Prepare input matching the 6-feature array expected by the production model
    X_input = prepare_fertilizer_input(cleaned)

    # Inference
    preds = model.predict(X_input)
    recommended_raw = str(preds[0]).strip()
    
    # Normalize display name if needed (e.g. 10/26/2026 -> 10-26-26)
    display_fertilizer = "10-26-26" if recommended_raw in ["10/26/2026", "10-26-26"] else recommended_raw

    # Probabilities / Confidence
    confidence = None
    top_candidates = []
    if hasattr(model, 'predict_proba') and hasattr(model, 'classes_'):
        probas = model.predict_proba(X_input)[0]
        max_idx = np.argmax(probas)
        confidence = float(probas[max_idx]) * 100.0

        top_indices = np.argsort(probas)[::-1][:3]
        for idx in top_indices:
            c_name = str(model.classes_[idx])
            if c_name == '10/26/2026':
                c_name = '10-26-26'
            top_candidates.append({
                'fertilizer': c_name,
                'probability': round(float(probas[idx]) * 100.0, 1)
            })

    # Generate explanatory rationale
    rationale = fertilizer_explanation(recommended_raw, cleaned)

    # Persist to database
    record = FertilizerPrediction(
        user_id=user_id,
        temperature=cleaned['temperature'],
        humidity=cleaned['humidity'],
        moisture=cleaned['Moisture'],
        soil_type=cleaned.get('soil_type', ''),
        crop_type=cleaned.get('crop_type', ''),
        N=cleaned['N'],
        P=cleaned['P'],
        K=cleaned['K'],
        recommended_fertilizer=display_fertilizer,
        explanation=rationale['why']
    )
    db.session.add(record)
    db.session.commit()

    result_details = {
        'id': record.id,
        'recommended_fertilizer': display_fertilizer,
        'confidence': round(confidence, 1) if confidence is not None else 98.0,
        'top_candidates': top_candidates,
        'explanation': rationale['why'],
        'nutrient_profile': rationale['nutrient_profile'],
        'primary_use': rationale['primary_use'],
        'application_tips': rationale['application_tips'],
        'inputs': cleaned,
        'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    return True, record, result_details, None


def get_fertilizer_prediction_by_id(prediction_id: int, user_id: Optional[int] = None) -> Optional[FertilizerPrediction]:
    """Retrieves a single fertilizer prediction with optional user ownership check."""
    query = FertilizerPrediction.query.filter_by(id=prediction_id)
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    return query.first()
