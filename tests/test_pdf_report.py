"""
PDF Report Generation Tests for AGRI-MITRA
Tests ReportLab generation for Crop Prediction and Fertilizer Recommendation.
"""

import unittest
from app import create_app
from database.db import db
from models.database_models import User, CropPrediction, FertilizerPrediction
from services.report_service import generate_crop_report_pdf, generate_fertilizer_report_pdf


class TestPDFReportService(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(full_name='Report Tester', email='rep@test.com', location='Punjab')
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
            N=37, P=0, K=0, recommended_fertilizer='Urea', explanation='Nitrogen deficit observed'
        )
        db.session.add_all([self.cp, self.fp])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_generate_crop_pdf(self):
        pdf_bytes = generate_crop_report_pdf(self.cp, self.user)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(len(pdf_bytes) > 500)
        # Standard PDF file header
        self.assertTrue(pdf_bytes.startswith(b'%PDF'))

    def test_generate_fertilizer_pdf(self):
        pdf_bytes = generate_fertilizer_report_pdf(self.fp, self.user)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(len(pdf_bytes) > 500)
        self.assertTrue(pdf_bytes.startswith(b'%PDF'))


if __name__ == '__main__':
    unittest.main()
