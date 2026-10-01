"""
Database Tests for AGRI-MITRA
Tests database models, constraints, password hashing, and relationships.
"""

import unittest
from app import create_app
from database.db import db
from models.database_models import User, CropPrediction, FertilizerPrediction


class TestDatabaseModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation_and_password_hashing(self):
        user = User(full_name='Test Farmer', email='farmer@test.com', role='user')
        user.set_password('Secret123!')
        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('Secret123!'))
        self.assertFalse(user.check_password('WrongPassword'))
        self.assertFalse(user.is_admin)

    def test_crop_prediction_relationship(self):
        user = User(full_name='Crop Farmer', email='crop@test.com')
        user.set_password('Pass123!')
        db.session.add(user)
        db.session.commit()

        pred = CropPrediction(
            user_id=user.id,
            N=90, P=42, K=43,
            temperature=20.8, humidity=82.0, ph=6.5, rainfall=202.9,
            predicted_crop='rice',
            fertilizer_suggestion='NPK 120:60:60'
        )
        db.session.add(pred)
        db.session.commit()

        self.assertEqual(len(user.crop_predictions), 1)
        self.assertEqual(user.crop_predictions[0].predicted_crop, 'rice')

    def test_fertilizer_prediction_relationship(self):
        user = User(full_name='Fertilizer Farmer', email='fert@test.com')
        user.set_password('Pass123!')
        db.session.add(user)
        db.session.commit()

        pred = FertilizerPrediction(
            user_id=user.id,
            temperature=26, humidity=52, moisture=38,
            soil_type='Sandy', crop_type='Maize',
            N=37, P=0, K=0,
            recommended_fertilizer='Urea',
            explanation='High nitrogen deficiency detected'
        )
        db.session.add(pred)
        db.session.commit()

        self.assertEqual(len(user.fertilizer_predictions), 1)
        self.assertEqual(user.fertilizer_predictions[0].recommended_fertilizer, 'Urea')


if __name__ == '__main__':
    unittest.main()
