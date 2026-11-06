"""
Admin Service & Operations Tests for AGRI-MITRA
Tests dashboard metrics, top crops, top fertilizers, 7-day analytics,
and user predictions queries.
"""

import unittest
from datetime import datetime
from app import create_app
from database.db import db
from models.database_models import User, CropPrediction, FertilizerPrediction
from services.admin_service import (
    get_dashboard_summary, get_top_crops, get_top_fertilizers,
    get_seven_day_analytics, get_all_user_predictions, get_user_contact_details
)


class TestAdminService(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed admin and regular user
        self.admin = User(full_name='Admin Boss', email='admin@test.com', role='admin')
        self.admin.set_password('AdminPass1!')
        self.user = User(full_name='Farmer Ram', email='ram@test.com', role='user', phone='98765', location='Punjab')
        self.user.set_password('RamPass1!')
        db.session.add_all([self.admin, self.user])
        db.session.commit()

        # Seed predictions
        c1 = CropPrediction(user_id=self.user.id, N=90, P=40, K=40, temperature=22, humidity=80, ph=6.5, rainfall=200, predicted_crop='rice')
        c2 = CropPrediction(user_id=self.user.id, N=90, P=40, K=40, temperature=22, humidity=80, ph=6.5, rainfall=200, predicted_crop='rice')
        f1 = FertilizerPrediction(user_id=self.user.id, temperature=26, humidity=52, moisture=38, N=37, P=0, K=0, recommended_fertilizer='Urea')
        db.session.add_all([c1, c2, f1])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_dashboard_summary(self):
        summary = get_dashboard_summary()
        self.assertEqual(summary['total_users'], 1)  # excludes admin
        self.assertEqual(summary['total_crop_predictions'], 2)
        self.assertEqual(summary['total_fertilizer_recommendations'], 1)
        self.assertEqual(summary['total_predictions'], 3)

    def test_top_crops(self):
        top = get_top_crops(limit=5)
        self.assertTrue(len(top) >= 1)
        self.assertEqual(top[0]['crop'], 'Rice')
        self.assertEqual(top[0]['count'], 2)

    def test_top_fertilizers(self):
        top = get_top_fertilizers(limit=5)
        self.assertTrue(len(top) >= 1)
        self.assertEqual(top[0]['fertilizer'], 'Urea')
        self.assertEqual(top[0]['count'], 1)

    def test_seven_day_analytics(self):
        analytics = get_seven_day_analytics()
        self.assertEqual(len(analytics['labels']), 7)
        self.assertEqual(len(analytics['crop_counts']), 7)
        self.assertEqual(len(analytics['fertilizer_counts']), 7)
        self.assertEqual(analytics['total_recent_crop'], 2)
        self.assertEqual(analytics['total_recent_fert'], 1)

    def test_user_contact_details(self):
        details = get_user_contact_details(search_query='Ram')
        self.assertEqual(len(details), 1)
        self.assertEqual(details[0]['full_name'], 'Farmer Ram')
        self.assertEqual(details[0]['phone'], '98765')


if __name__ == '__main__':
    unittest.main()
