"""
Fertilizer Recommendation Model & Advisory Tests for AGRI-MITRA
Tests input validation, ML model inference, explanation generation,
and database persistence.
"""

import unittest
from app import create_app
from database.db import db
from models.database_models import User, FertilizerPrediction
from services.fertilizer_recommendation_service import predict_fertilizer


class TestFertilizerRecommendation(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(full_name='Fertilizer Test Farmer', email='ferttest@farm.com')
        self.user.set_password('Pass1234')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fertilizer_recommendation_valid(self):
        # Sample for Urea profile from raw dataset: [26, 52, 38, 'Sandy', 'Maize', 37, 0, 0]
        payload = {
            'temperature': 26,
            'humidity': 52,
            'Moisture': 38,
            'soil_type': 'Sandy',
            'crop_type': 'Maize',
            'N': 37,
            'P': 0,
            'K': 0
        }

        success, record, details, err = predict_fertilizer(payload, user_id=self.user.id)
        self.assertTrue(success)
        self.assertIsNone(err)
        self.assertIsNotNone(record)
        self.assertEqual(record.recommended_fertilizer, 'Urea')
        self.assertIn('nitrogen', record.explanation.lower())

        # Check DB persistence
        saved = FertilizerPrediction.query.get(record.id)
        self.assertIsNotNone(saved)
        self.assertEqual(saved.recommended_fertilizer, 'Urea')

    def test_fertilizer_recommendation_validation_error(self):
        payload = {'temperature': 26}
        success, record, details, err = predict_fertilizer(payload, user_id=self.user.id)
        self.assertFalse(success)
        self.assertIn("required", err)


if __name__ == '__main__':
    unittest.main()
