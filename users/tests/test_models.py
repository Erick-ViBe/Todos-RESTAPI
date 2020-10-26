from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_successful(self):
        """Test creating a new custom TodoUser is successfully"""
        username = 'usernametest'
        password = 'testpassword'
        color = 'Blue'

        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            color=color
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.color, color)
        self.assertTrue(user.check_password(password))
