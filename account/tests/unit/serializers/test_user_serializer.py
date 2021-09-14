from unittest import TestCase
from rest_framework.serializers import ValidationError

from account.serializers.user_serializer import UserSerializer

class TestUserSerializer(TestCase):
    def setUp(self) -> None:
        self.serializer = UserSerializer()

    def test_password_validation_invalid_input(self):
        values = {
            'password': 'test1',
            'password2': 'test2'
        }
        
        with self.assertRaises(ValidationError) as ctx:
            self.serializer.validate(values)

        self.assertEqual(ctx.exception.detail, {"password": ["Passwords do not match."]})
