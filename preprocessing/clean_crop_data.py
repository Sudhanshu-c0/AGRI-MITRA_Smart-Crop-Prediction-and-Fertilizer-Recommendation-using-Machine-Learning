"""
Clean Crop Data Module for AGRI-MITRA
Cleans raw crop dataset and exports to datasets/cleaned/crop_cleaned.csv.
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
from preprocessing.data_validation import validate_crop_dataset
RAW_PATH = BASE_DIR / 'datasets' / 'raw' / 'crop_dataset.csv'
CLEANED_PATH = BASE_DIR / 'datasets' / 'cleaned' / 'crop_cleaned.csv'


def clean_crop_dataset(raw_path: Path = RAW_PATH, out_path: Path = CLEANED_PATH) -> pd.DataFrame:
    """Cleans raw crop dataset safely, preserving data integrity."""
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw crop dataset not found at: {raw_path}")

    df = pd.read_csv(raw_path)
    
    # 1. Normalize column names (strip whitespace)
    df.columns = df.columns.str.strip()

    # 2. Strip string values in target label
    if 'label' in df.columns:
        df['label'] = df['label'].astype(str).str.strip().str.lower()

    # 3. Ensure numeric types
    numeric_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Handle any missing values if present (impute by median per crop or drop if target null)
    df = df.dropna(subset=['label'])
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df.groupby('label')[col].transform(lambda grp: grp.fillna(grp.median()))

    # 5. Remove any exact duplicate rows
    df = df.drop_duplicates().reset_index(drop=True)

    # 6. Validate
    val_report = validate_crop_dataset(df)
    if not val_report['is_valid']:
        raise ValueError(f"Cleaned crop data failed validation: {val_report['errors']}")

    # 7. Save cleaned dataset
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"[OK] Saved cleaned crop dataset: {out_path} ({len(df)} rows)")
    return df


if __name__ == '__main__':
    clean_crop_dataset()
