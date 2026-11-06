"""
Crop Prediction Model & Pipeline Tests for AGRI-MITRA
Tests input validation, ML model inference, baseline fertilizer generation,
and database persistence.
"""

import unittest
from app import create_app
from database.db import db
from models.database_models import User, CropPrediction
from services.crop_prediction_service import predict_crop


class TestCropPrediction(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed test user
        self.user = User(full_name='Crop Test Farmer', email='croptest@farm.com')
        self.user.set_password('Pass1234')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crop_prediction_valid_input(self):
        # Rice profile inputs
        payload = {
            'N': 90,
            'P': 42,
            'K': 43,
            'temperature': 20.87,
            'humidity': 82.0,
            'ph': 6.5,
            'rainfall': 202.9
        }

        success, record, details, err = predict_crop(payload, user_id=self.user.id)
        self.assertTrue(success)
        self.assertIsNone(err)
        self.assertIsNotNone(record)
        self.assertEqual(record.predicted_crop.lower(), 'rice')
        self.assertIn('NPK', record.fertilizer_suggestion)

        # Check DB persistence
        saved = CropPrediction.query.get(record.id)
        self.assertIsNotNone(saved)
        self.assertEqual(saved.predicted_crop.lower(), 'rice')

    def test_crop_prediction_invalid_input(self):
        # Missing fields
        payload = {'N': 90, 'P': 42}
        success, record, details, err = predict_crop(payload, user_id=self.user.id)
        self.assertFalse(success)
        self.assertIn("Field 'K' is required", err)


if __name__ == '__main__':
    unittest.main()
