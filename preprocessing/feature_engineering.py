"""
Feature Engineering Module for AGRI-MITRA
Extracts and structures features exactly as required by production models.
Produces datasets/processed/crop_features.csv and datasets/processed/fertilizer_features.csv.
"""

from pathlib import Path
from typing import Dict, Any, List, Union
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]

CROP_FEATURES = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
FERTILIZER_FEATURES = ['temperature', 'humidity', 'Moisture', 'N', 'K', 'P']


def process_crop_features(
    cleaned_path: Path = BASE_DIR / 'datasets' / 'cleaned' / 'crop_cleaned.csv',
    processed_path: Path = BASE_DIR / 'datasets' / 'processed' / 'crop_features.csv'
) -> pd.DataFrame:
    """Processes cleaned crop data into features dataset preserving exact model feature order."""
    if not cleaned_path.exists():
        raise FileNotFoundError(f"Cleaned crop data not found at: {cleaned_path}")

    df = pd.read_csv(cleaned_path)
    df.columns = df.columns.str.strip()

    # Verify features exist
    for col in CROP_FEATURES:
        if col not in df.columns:
            raise KeyError(f"Feature column '{col}' missing from cleaned crop data.")

    # Include target if available
    cols_to_export = list(CROP_FEATURES)
    if 'label' in df.columns:
        cols_to_export.append('label')

    processed_df = df[cols_to_export].copy()
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(processed_path, index=False)
    print(f"[OK] Saved processed crop features: {processed_path} ({len(processed_df)} rows)")
    return processed_df


def process_fertilizer_features(
    cleaned_path: Path = BASE_DIR / 'datasets' / 'cleaned' / 'fertilizer_cleaned.csv',
    processed_path: Path = BASE_DIR / 'datasets' / 'processed' / 'fertilizer_features.csv'
) -> pd.DataFrame:
    """Processes cleaned fertilizer data into features dataset preserving exact model feature order."""
    if not cleaned_path.exists():
        raise FileNotFoundError(f"Cleaned fertilizer data not found at: {cleaned_path}")

    df = pd.read_csv(cleaned_path)
    df.columns = df.columns.str.strip()

    for col in FERTILIZER_FEATURES:
        if col not in df.columns:
            raise KeyError(f"Feature column '{col}' missing from cleaned fertilizer data.")

    cols_to_export = list(FERTILIZER_FEATURES)
    if 'Fertilizer Name' in df.columns:
        cols_to_export.append('Fertilizer Name')

    processed_df = df[cols_to_export].copy()
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(processed_path, index=False)
    print(f"[OK] Saved processed fertilizer features: {processed_path} ({len(processed_df)} rows)")
    return processed_df


def prepare_crop_input(user_input: Dict[str, Any]) -> pd.DataFrame:
    """
    Transforms user input dictionary into a 1-row DataFrame matching the
    exact feature names and order expected by the Crop RandomForest model.
    """
    data = {
        'N': [float(user_input['N'])],
        'P': [float(user_input['P'])],
        'K': [float(user_input['K'])],
        'temperature': [float(user_input['temperature'])],
        'humidity': [float(user_input['humidity'])],
        'ph': [float(user_input['ph'])],
        'rainfall': [float(user_input['rainfall'])],
    }
    return pd.DataFrame(data, columns=CROP_FEATURES)


def prepare_fertilizer_input(user_input: Dict[str, Any]) -> np.ndarray:
    """
    Transforms user input dictionary into a 2D numpy array matching the
    exact 6 features expected by the supplied Fertilizer RandomForest model:
    [temperature, humidity, Moisture, N, K, K].
    (Note: The supplied model was trained with 6 features where index 4 and 5 are K values).
    """
    temp = float(user_input['temperature'])
    hum = float(user_input['humidity'])
    moist = float(user_input.get('Moisture', user_input.get('moisture', 40.0)))
    n = float(user_input['N'])
    k = float(user_input['K'])

    # Supplied model input layout: 6 numerical features
    return np.array([[temp, hum, moist, n, k, k]], dtype=np.float64)


if __name__ == '__main__':
    process_crop_features()
    process_fertilizer_features()
