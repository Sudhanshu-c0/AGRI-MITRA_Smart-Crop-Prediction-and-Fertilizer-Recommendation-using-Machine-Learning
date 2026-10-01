"""
History Management Tests for AGRI-MITRA
Tests retrieving user crop history, fertilizer history, combined history, and deletion.
"""

import unittest
from app import create_app
from database.db import db
from models.database_models import User, CropPrediction, FertilizerPrediction
from services.history_service import (
    get_user_crop_history, get_user_fertilizer_history,
    get_user_combined_history, delete_crop_prediction
)


class TestHistoryService(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(full_name='History User', email='hist@test.com')
        self.user.set_password('Pass1234')
        db.session.add(self.user)
        db.session.commit()

        # Seed records
        cp = CropPrediction(
            user_id=self.user.id,
            N=80, P=40, K=40, temperature=25, humidity=80, ph=6.5, rainfall=200,
            predicted_crop='rice', fertilizer_suggestion='NPK baseline'
        )
        fp = FertilizerPrediction(
            user_id=self.user.id,
            temperature=28, humidity=60, moisture=45, soil_type='Loamy', crop_type='Wheat',
            N=12, P=36, K=0, recommended_fertilizer='DAP', explanation='Phosphate boost'
        )
        db.session.add_all([cp, fp])
        db.session.commit()
        self.cp_id = cp.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_combined_history(self):
        combined = get_user_combined_history(self.user.id)
        self.assertEqual(len(combined), 2)
        categories = {item['category'] for item in combined}
        self.assertEqual(categories, {'crop', 'fertilizer'})

    def test_delete_history_item(self):
        del_res = delete_crop_prediction(self.cp_id, self.user.id)
        self.assertTrue(del_res)
        crops = get_user_crop_history(self.user.id)
        self.assertEqual(len(crops), 0)


if __name__ == '__main__':
    unittest.main()
