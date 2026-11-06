"""
Reproducibility Training Script for Fertilizer Model
Trains a candidate model on datasets/cleaned/fertilizer_cleaned.csv and saves to models/candidate/.
Does NOT overwrite the production Fertilizer_Recommendation_RF.pkl model.
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATA_PATH = BASE_DIR / 'datasets' / 'cleaned' / 'fertilizer_cleaned.csv'
CANDIDATE_DIR = BASE_DIR / 'models' / 'candidate'


def train_fertilizer_candidate():
    print("[TRAIN] Starting Fertilizer Model training run...")
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Cleaned data not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    # Supplied production model layout: 6 numerical features [temperature, humidity, Moisture, N, K, K]
    X = df[['temperature', 'humidity', 'Moisture', 'N', 'K', 'K']].values
    y = df['Fertilizer Name']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    train_acc = accuracy_score(y_train, clf.predict(X_train))
    test_acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"[TRAIN] Fertilizer Candidate Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}")

    CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
    out_candidate = CANDIDATE_DIR / 'Fertilizer_Recommendation_RF_candidate.pkl'
    bundle = {
        'model': clf,
        'features': ['temperature', 'humidity', 'Moisture', 'N', 'K', 'K'],
        'classes': clf.classes_
    }
    with open(out_candidate, 'wb') as f:
        pickle.dump(bundle, f)
    print(f"[OK] Candidate model saved to: {out_candidate}")
    return out_candidate


if __name__ == '__main__':
    train_fertilizer_candidate()
