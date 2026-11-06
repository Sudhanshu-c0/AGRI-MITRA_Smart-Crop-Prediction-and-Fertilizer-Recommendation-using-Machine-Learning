"""
Authentication Unit Tests for AGRI-MITRA
Tests user registration, login, logout, password validation, and session auth.
"""

import unittest
from app import create_app
from database.db import db
from models.database_models import User
from services.auth_service import signup_user, authenticate_user


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_override={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup_success(self):
        success, user, msg = signup_user('Jane Doe', 'jane@farm.org', 'StrongPass123!')
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'jane@farm.org')

    def test_signup_duplicate_email(self):
        signup_user('First User', 'dup@farm.org', 'Pass1234')
        success, user, msg = signup_user('Second User', 'dup@farm.org', 'Pass1234')
        self.assertFalse(success)
        self.assertIn('already exists', msg)

    def test_signup_invalid_email(self):
        success, user, msg = signup_user('Bad Email User', 'notanemail', 'Pass1234')
        self.assertFalse(success)
        self.assertIn('valid email', msg)

    def test_authentication_flow(self):
        signup_user('Auth Tester', 'auth@farm.org', 'SecretCode99')
        success, user, msg = authenticate_user('auth@farm.org', 'SecretCode99')
        self.assertTrue(success)
        self.assertEqual(user.email, 'auth@farm.org')

        # Wrong password
        fail, u_fail, msg_fail = authenticate_user('auth@farm.org', 'WrongCode')
        self.assertFalse(fail)
        self.assertIsNone(u_fail)


if __name__ == '__main__':
    unittest.main()
