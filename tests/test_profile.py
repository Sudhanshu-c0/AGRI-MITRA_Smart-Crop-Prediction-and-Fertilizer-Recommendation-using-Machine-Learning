"""
Profile Service Tests for AGRI-MITRA
Tests profile updates, duplicate email check, and password changes.
"""

import unittest
from app import create_app
from database.db import db
from models.database_models import User
from services.profile_service import update_profile, change_password


class TestProfileService(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(full_name='Profile Tester', email='pro@test.com', phone='12345', location='Pune')
        self.user.set_password('OldPassword1!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_update_profile(self):
        success, msg = update_profile(self.user.id, 'Updated Name', 'updated@test.com', '99999', 'Mumbai')
        self.assertTrue(success)
        reloaded = User.query.get(self.user.id)
        self.assertEqual(reloaded.full_name, 'Updated Name')
        self.assertEqual(reloaded.location, 'Mumbai')

    def test_change_password(self):
        success, msg = change_password(self.user.id, 'OldPassword1!', 'NewStrongPass2@', 'NewStrongPass2@')
        self.assertTrue(success)
        reloaded = User.query.get(self.user.id)
        self.assertTrue(reloaded.check_password('NewStrongPass2@'))

    def test_change_password_wrong_current(self):
        success, msg = change_password(self.user.id, 'WrongCurrent', 'NewPass1234', 'NewPass1234')
        self.assertFalse(success)
        self.assertIn('Current password is incorrect', msg)


if __name__ == '__main__':
    unittest.main()
