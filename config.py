import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'agri-mitra-secure-secret-key-2026')
    
    # Database
    db_env_url = os.getenv('DATABASE_URL')
    if db_env_url and db_env_url.startswith('sqlite:///') and not os.path.isabs(db_env_url.replace('sqlite:///', '')):
        # Make sure sqlite database is placed cleanly in instance/agri_mitra.db
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'agri_mitra.db'}"
    elif db_env_url:
        SQLALCHEMY_DATABASE_URI = db_env_url
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'agri_mitra.db'}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin Credentials
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@agrimitra.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'ChangeThisAdminPassword!2026')

    # Machine Learning Model Artifacts
    CROP_MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'Crop_Prediction_RF.pkl'
    FERTILIZER_MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'Fertilizer_Recommendation_RF.pkl'
    CROP_ENCODER_PATH = BASE_DIR / 'models' / 'ml' / 'crop_encoder.pkl'
    FERTILIZER_ENCODER_PATH = BASE_DIR / 'models' / 'ml' / 'fertilizer_encoder.pkl'
    METADATA_PATH = BASE_DIR / 'models' / 'ml' / 'model_metadata.json'

    # Storage Dirs
    REPORT_DIR = BASE_DIR / 'reports' / 'generated'
    EXPORT_DIR = BASE_DIR / 'exports'
    UPLOAD_DIR = BASE_DIR / 'uploads'
