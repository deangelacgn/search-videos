import pytest
from django.test import Client


@pytest.mark.django_db
@pytest.mark.integration
class TestObtainTokenEndpoint:
    user_endpoint = '/api/user/'
    obtain_token_endpoint = '/api/login/'
    default_user_params =  {
        'email': 'test@test.com',
        'username': 'test',
        'first_name': 'test name',
        'last_name': 'test surname',
        'password': 'test1234',
        'password2': 'test1234'
    }

    @pytest.mark.parametrize(
        ('user_identification', 'password', 'status_code', 'expected_fields'),
        [
            ('test', 'test1234', 200, ['user', 'access', 'refresh']),
        ]
    )
    def test_login_success(self, user_identification, password, status_code, expected_fields):
        signup_response = Client().post(
            path=self.user_endpoint,
            data=self.default_user_params
        )

        created_user = signup_response.json()

        login_response = Client().post(
            path=self.obtain_token_endpoint,
            data={
                'username': user_identification,
                'password': password
            }
        )

        assert login_response.status_code == status_code
        response_json = login_response.json()

        for field in expected_fields:
            assert field in response_json
        
        logged_user = response_json['user']
        assert logged_user == created_user

    @pytest.mark.parametrize(
        ('login_credentials', 'status_code', 'error_msg'),
        [
           ({'username': 'ttest', 'password': 'test1234'}, 401, 'No active account found with the given credentials'),
           ({'username': 'test', 'password': '1234'}, 401, 'No active account found with the given credentials')
        ]
    )
    def test_user_login_invalid(self, login_credentials, status_code, error_msg):
        response = Client().post(
            path=self.user_endpoint,
            data=self.default_user_params
        )

        login_response = Client().post(
            path=self.obtain_token_endpoint,
            data=login_credentials
        )

        assert login_response.status_code == status_code
        response_json = login_response.json()

        assert response_json['detail'] == error_msg
