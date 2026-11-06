"""
Database Models for AGRI-MITRA
Defines User, CropPrediction, and FertilizerPrediction models.
"""

from datetime import datetime
from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30), nullable=True, default='')
    location = db.Column(db.String(120), nullable=True, default='')
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    crop_predictions = db.relationship('CropPrediction', backref='user', lazy=True, cascade='all, delete-orphan')
    fertilizer_predictions = db.relationship('FertilizerPrediction', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == 'admin'

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }


class CropPrediction(db.Model):
    __tablename__ = 'crop_prediction'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    
    # Soil & Environmental Parameters
    N = db.Column(db.Float, nullable=False)
    P = db.Column(db.Float, nullable=False)
    K = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    
    # Prediction Results
    predicted_crop = db.Column(db.String(80), nullable=False, index=True)
    fertilizer_suggestion = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else 'Unknown',
            'user_email': self.user.email if self.user else 'Unknown',
            'N': self.N,
            'P': self.P,
            'K': self.K,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'ph': self.ph,
            'rainfall': self.rainfall,
            'predicted_crop': self.predicted_crop,
            'fertilizer_suggestion': self.fertilizer_suggestion,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }


class FertilizerPrediction(db.Model):
    __tablename__ = 'fertilizer_prediction'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    # Parameters
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Float, nullable=False)
    soil_type = db.Column(db.String(80), nullable=True, default='')
    crop_type = db.Column(db.String(80), nullable=True, default='')
    N = db.Column(db.Float, nullable=False)
    P = db.Column(db.Float, nullable=False)
    K = db.Column(db.Float, nullable=False)

    # Recommendation Results
    recommended_fertilizer = db.Column(db.String(120), nullable=False, index=True)
    explanation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else 'Unknown',
            'user_email': self.user.email if self.user else 'Unknown',
            'temperature': self.temperature,
            'humidity': self.humidity,
            'moisture': self.moisture,
            'soil_type': self.soil_type,
            'crop_type': self.crop_type,
            'N': self.N,
            'P': self.P,
            'K': self.K,
            'recommended_fertilizer': self.recommended_fertilizer,
            'explanation': self.explanation,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }
