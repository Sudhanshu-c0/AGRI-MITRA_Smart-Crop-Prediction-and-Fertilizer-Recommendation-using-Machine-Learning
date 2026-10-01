"""
CSV Export Tests for AGRI-MITRA
Tests streaming CSV export for crops, fertilizers, combined history, and users.
"""

import unittest
from app import create_app
from database.db import db
from models.database_models import User, CropPrediction, FertilizerPrediction
from services.csv_export_service import (
    export_crop_predictions_csv,
    export_fertilizer_predictions_csv,
    export_combined_history_csv,
    export_users_csv
)


class TestCSVExportService(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(full_name='CSV Tester', email='csv@test.com', phone='1234567890', location='Haryana')
        self.user.set_password('Pass1234')
        db.session.add(self.user)
        db.session.commit()

        self.cp = CropPrediction(
            user_id=self.user.id,
            N=90, P=42, K=43, temperature=20.8, humidity=82.0, ph=6.5, rainfall=202.9,
            predicted_crop='rice', fertilizer_suggestion='NPK 120:60:60'
        )
        self.fp = FertilizerPrediction(
            user_id=self.user.id,
            temperature=26, humidity=52, moisture=38, soil_type='Sandy', crop_type='Maize',
            N=37, P=0, K=0, recommended_fertilizer='Urea', explanation='Nitrogen deficit'
        )
        db.session.add_all([self.cp, self.fp])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_export_crop_csv(self):
        resp = export_crop_predictions_csv(self.user.id)
        self.assertEqual(resp.mimetype, 'text/csv')
        data = resp.get_data(as_text=True)
        self.assertIn('Nitrogen (N)', data)
        self.assertIn('Rice', data)

    def test_export_fertilizer_csv(self):
        resp = export_fertilizer_predictions_csv(self.user.id)
        self.assertEqual(resp.mimetype, 'text/csv')
        data = resp.get_data(as_text=True)
        self.assertIn('Recommended Fertilizer', data)
        self.assertIn('Urea', data)

    def test_export_combined_history_csv(self):
        resp = export_combined_history_csv(self.user.id)
        data = resp.get_data(as_text=True)
        self.assertIn('Record Type', data)
        self.assertIn('Crop Prediction', data)
        self.assertIn('Fertilizer Recommendation', data)

    def test_export_users_csv(self):
        resp = export_users_csv()
        data = resp.get_data(as_text=True)
        self.assertIn('Full Name', data)
        self.assertIn('CSV Tester', data)


if __name__ == '__main__':
    unittest.main()
