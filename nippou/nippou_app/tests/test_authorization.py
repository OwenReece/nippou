from django.test import TestCase
from ..logic import authorization


class AuthorizationTestCase(TestCase):
    TEST_USER = {
        "email": "test@test.com",
        "password": "password0",
        "password_confirm": "password0"
    }

    def setUp(self):
        user = authorization.signup(self.TEST_USER)
        self.assertTrue(user)

    def test_authorize(self):
        user = authorization.authorize(self.TEST_USER)
        self.assertTrue(user)

    def test_user_email(self):
        invalid = {
            "email": "test@test",
            "password": "password0",
            "password_confirm": "password0"
        }

        self.assertRaises(Exception, lambda: authorization.signup(invalid))

    def test_user_password_length(self):
        invalid = {
            "email": "test@test.com",
            "password": "pass0",
            "password_confirm": "pass0"
        }
        self.assertRaises(Exception, lambda: authorization.signup(invalid))

    def test_user_password_variety(self):
        invalid = {
            "email": "test@test.com",
            "password": "password",
            "password_confirm": "password"
        }
        self.assertRaises(Exception, lambda: authorization.signup(invalid))

    def test_user_password_match(self):
        invalid = {
            "email": "test@test.com",
            "password": "password0",
            "password_confirm": "password1"
        }
        self.assertRaises(Exception, lambda: authorization.signup(invalid))
