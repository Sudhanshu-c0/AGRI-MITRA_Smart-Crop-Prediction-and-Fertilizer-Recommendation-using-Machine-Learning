"""
Data Validation Module for AGRI-MITRA
Validates raw/cleaned datasets and incoming inference payloads for both
Crop Prediction and Fertilizer Recommendation pipelines.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, List, Union
import pandas as pd
import numpy as np

# Crop feature boundaries based on agronomic realities and training distributions
CROP_NUMERIC_RANGES = {
    'N': (0.0, 300.0),           # Nitrogen ratio (kg/ha equivalent)
    'P': (0.0, 300.0),           # Phosphorus ratio (kg/ha equivalent)
    'K': (0.0, 300.0),           # Potassium ratio (kg/ha equivalent)
    'temperature': (-10.0, 60.0),# Ambient temperature in Celsius
    'humidity': (0.0, 100.0),    # Relative humidity in percentage
    'ph': (0.0, 14.0),           # Soil pH scale
    'rainfall': (0.0, 1000.0),   # Rainfall in mm
}

# Fertilizer feature boundaries
FERTILIZER_NUMERIC_RANGES = {
    'temperature': (0.0, 60.0),
    'humidity': (0.0, 100.0),
    'Moisture': (0.0, 100.0),
    'N': (0.0, 200.0),
    'K': (0.0, 200.0),
    'P': (0.0, 200.0),
}

VALID_SOIL_TYPES = {'Sandy', 'Loamy', 'Black', 'Red', 'Clayey'}
VALID_CROP_TYPES = {
    'Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy',
    'Barley', 'Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts'
}

VALID_FERTILIZERS = {'Urea', 'DAP', '14-35-14', '28-28', '17-17-17', '20-20', '10/26/2026'}


def validate_crop_dataset(data: Union[str, Path, pd.DataFrame]) -> Dict[str, Any]:
    """Validates the raw or cleaned Crop dataset."""
    if isinstance(data, (str, Path)):
        df = pd.read_csv(data)
    else:
        df = data.copy()

    df.columns = df.columns.str.strip()
    required = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
    missing_cols = [c for c in required if c not in df.columns]
    
    errors: List[str] = []
    warnings: List[str] = []

    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        return {'is_valid': False, 'errors': errors, 'warnings': warnings, 'rows': len(df)}

    # Check nulls
    null_counts = df[required].isnull().sum().to_dict()
    has_nulls = any(v > 0 for v in null_counts.values())
    if has_nulls:
        errors.append(f"Missing values detected: {null_counts}")

    # Check numeric types and ranges
    for col, (min_v, max_v) in CROP_NUMERIC_RANGES.items():
        if not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"Column '{col}' is not numeric.")
        else:
            out_of_bounds = df[(df[col] < min_v) | (df[col] > max_v)]
            if len(out_of_bounds) > 0:
                warnings.append(f"{len(out_of_bounds)} rows in '{col}' fall outside range [{min_v}, {max_v}].")

    # Check target
    target_uniques = df['label'].dropna().unique().tolist()
    if len(target_uniques) < 2:
        errors.append("Dataset target column 'label' has fewer than 2 unique classes.")

    duplicates = int(df.duplicated().sum())
    if duplicates > 0:
        warnings.append(f"{duplicates} duplicate rows found in dataset.")

    is_valid = len(errors) == 0
    return {
        'is_valid': is_valid,
        'errors': errors,
        'warnings': warnings,
        'rows': int(len(df)),
        'unique_classes': len(target_uniques),
        'duplicates': duplicates,
    }


def validate_fertilizer_dataset(data: Union[str, Path, pd.DataFrame]) -> Dict[str, Any]:
    """Validates the raw or cleaned Fertilizer dataset."""
    if isinstance(data, (str, Path)):
        df = pd.read_csv(data)
    else:
        df = data.copy()

    df.columns = df.columns.str.strip()
    required = ['temperature', 'humidity', 'Moisture', 'Soil Type', 'Crop Type', 'N', 'K', 'P', 'Fertilizer Name']
    missing_cols = [c for c in required if c not in df.columns]

    errors: List[str] = []
    warnings: List[str] = []

    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        return {'is_valid': False, 'errors': errors, 'warnings': warnings, 'rows': len(df)}

    # Check nulls
    null_counts = df[required].isnull().sum().to_dict()
    if any(v > 0 for v in null_counts.values()):
        errors.append(f"Missing values detected: {null_counts}")

    # Check numeric types and ranges
    for col, (min_v, max_v) in FERTILIZER_NUMERIC_RANGES.items():
        if not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"Column '{col}' is not numeric.")
        else:
            out_of_bounds = df[(df[col] < min_v) | (df[col] > max_v)]
            if len(out_of_bounds) > 0:
                warnings.append(f"{len(out_of_bounds)} rows in '{col}' fall outside range [{min_v}, {max_v}].")

    # Check target
    target_uniques = df['Fertilizer Name'].dropna().unique().tolist()
    if len(target_uniques) < 2:
        errors.append("Fertilizer target has fewer than 2 unique classes.")

    duplicates = int(df.duplicated().sum())
    if duplicates > 0:
        warnings.append(f"{duplicates} duplicate rows found in dataset.")

    is_valid = len(errors) == 0
    return {
        'is_valid': is_valid,
        'errors': errors,
        'warnings': warnings,
        'rows': int(len(df)),
        'unique_classes': len(target_uniques),
        'duplicates': duplicates,
    }


def validate_crop_input(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, float], List[str]]:
    """Validates user-submitted inputs for Crop Prediction."""
    cleaned: Dict[str, float] = {}
    errors: List[str] = []

    for field, (min_v, max_v) in CROP_NUMERIC_RANGES.items():
        if field not in payload or payload[field] is None or str(payload[field]).strip() == '':
            errors.append(f"Field '{field}' is required.")
            continue
        try:
            val = float(payload[field])
            if not np.isfinite(val):
                errors.append(f"Field '{field}' must be a finite number.")
            elif val < min_v or val > max_v:
                errors.append(f"Field '{field}' must be between {min_v} and {max_v}.")
            else:
                cleaned[field] = val
        except (ValueError, TypeError):
            errors.append(f"Field '{field}' must be a valid number.")

    return len(errors) == 0, cleaned, errors


def validate_fertilizer_input(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
    """Validates user-submitted inputs for Fertilizer Recommendation."""
    cleaned: Dict[str, Any] = {}
    errors: List[str] = []

    for field, (min_v, max_v) in FERTILIZER_NUMERIC_RANGES.items():
        # Allow case-insensitive key lookup for moisture
        key = field
        if key not in payload:
            alt_key = field.lower()
            if alt_key in payload:
                key = alt_key

        if key not in payload or payload[key] is None or str(payload[key]).strip() == '':
            errors.append(f"Numeric parameter '{field}' is required.")
            continue
        try:
            val = float(payload[key])
            if not np.isfinite(val):
                errors.append(f"Field '{field}' must be finite.")
            elif val < min_v or val > max_v:
                errors.append(f"Field '{field}' must be between {min_v} and {max_v}.")
            else:
                cleaned[field] = val
        except (ValueError, TypeError):
            errors.append(f"Field '{field}' must be a valid number.")

    # Soil type & crop type can be optional or validated against known list
    soil = payload.get('soil_type') or payload.get('Soil Type') or 'Loamy'
    crop_t = payload.get('crop_type') or payload.get('Crop Type') or 'Wheat'
    cleaned['soil_type'] = str(soil).strip()
    cleaned['crop_type'] = str(crop_t).strip()

    return len(errors) == 0, cleaned, errors
