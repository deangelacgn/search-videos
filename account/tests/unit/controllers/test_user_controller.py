from unittest import TestCase
from unittest.mock import MagicMock, patch

from account.controllers.user_controller import register_new_user


class TestSignUp(TestCase):
    @patch('account.controllers.user_controller.User.objects.create')
    def test_user_creation(self, mock_create_user):
        """ Test the flow of the registering a new user.
        """
        user_data = {
            'email': 'test@test.com',
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': '1234'
        }

        mock_user = MagicMock()
        mock_create_user.return_value = mock_user
        mock_user.set_password.return_value = MagicMock()

        register_new_user(user_data)

        mock_create_user.assert_called_once_with(
            email=user_data['email'],
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        mock_user.set_password.assert_called_once_with(user_data['password'])
