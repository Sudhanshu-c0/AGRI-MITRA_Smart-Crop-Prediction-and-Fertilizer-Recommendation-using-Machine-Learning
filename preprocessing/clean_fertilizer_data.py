"""
Clean Fertilizer Data Module for AGRI-MITRA
Cleans raw fertilizer dataset and exports to datasets/cleaned/fertilizer_cleaned.csv.
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
from preprocessing.data_validation import validate_fertilizer_dataset
RAW_PATH = BASE_DIR / 'datasets' / 'raw' / 'fertilizer_dataset.csv'
CLEANED_PATH = BASE_DIR / 'datasets' / 'cleaned' / 'fertilizer_cleaned.csv'


def clean_fertilizer_dataset(raw_path: Path = RAW_PATH, out_path: Path = CLEANED_PATH) -> pd.DataFrame:
    """Cleans raw fertilizer dataset safely, preserving data integrity."""
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw fertilizer dataset not found at: {raw_path}")

    df = pd.read_csv(raw_path)

    # 1. Normalize column names (strip whitespace e.g. 'humidity ')
    df.columns = df.columns.str.strip()

    # 2. Clean string categorical columns
    str_cols = ['Soil Type', 'Crop Type', 'Fertilizer Name']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 3. Numeric conversion
    numeric_cols = ['temperature', 'humidity', 'Moisture', 'N', 'K', 'P']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Handle missing values
    df = df.dropna(subset=['Fertilizer Name'])
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df.groupby('Fertilizer Name')[col].transform(lambda grp: grp.fillna(grp.median()))

    # 5. Drop exact duplicates if any
    df = df.drop_duplicates().reset_index(drop=True)

    # 6. Validate
    val_report = validate_fertilizer_dataset(df)
    if not val_report['is_valid']:
        raise ValueError(f"Cleaned fertilizer data failed validation: {val_report['errors']}")

    # 7. Save cleaned dataset
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"[OK] Saved cleaned fertilizer dataset: {out_path} ({len(df)} rows)")
    return df


if __name__ == '__main__':
    clean_fertilizer_dataset()
