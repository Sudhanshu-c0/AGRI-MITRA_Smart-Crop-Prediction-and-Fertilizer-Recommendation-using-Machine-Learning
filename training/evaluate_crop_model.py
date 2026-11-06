"""
Model Evaluation Script for Crop Prediction
Evaluates the production Crop_Prediction_RF.pkl model against datasets/cleaned/crop_cleaned.csv.
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pickle
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix
)

MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'Crop_Prediction_RF.pkl'
DATA_PATH = BASE_DIR / 'datasets' / 'cleaned' / 'crop_cleaned.csv'


def evaluate_crop_model():
    print("=" * 60)
    print("AGRI-MITRA: Evaluating Crop Prediction Model")
    print("=" * 60)

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at {DATA_PATH}")

    with open(MODEL_PATH, 'rb') as f:
        bundle = pickle.load(f)

    model = bundle['model'] if isinstance(bundle, dict) and 'model' in bundle else bundle
    df = pd.read_csv(DATA_PATH)
    
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[features]
    y_true = df['label']

    y_pred = model.predict(X)

    acc = accuracy_score(y_true, y_pred)
    prec_w = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec_w = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1_w = f1_score(y_true, y_pred, average='weighted', zero_division=0)

    prec_m = precision_score(y_true, y_pred, average='macro', zero_division=0)
    rec_m = recall_score(y_true, y_pred, average='macro', zero_division=0)
    f1_m = f1_score(y_true, y_pred, average='macro', zero_division=0)

    print(f"Total Samples Evaluated: {len(df)}")
    print(f"Accuracy:            {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision (Weighted): {prec_w:.4f}")
    print(f"Recall (Weighted):    {rec_w:.4f}")
    print(f"F1-Score (Weighted):  {f1_w:.4f}")
    print(f"F1-Score (Macro):     {f1_m:.4f}")
    print("-" * 60)
    print("Classification Report:")
    print(classification_report(y_true, y_pred, digits=4, zero_division=0))

    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix shape:", cm.shape)

    return {
        'accuracy': float(acc),
        'precision_weighted': float(prec_w),
        'recall_weighted': float(rec_w),
        'f1_weighted': float(f1_w),
        'f1_macro': float(f1_m),
    }


if __name__ == '__main__':
    evaluate_crop_model()
