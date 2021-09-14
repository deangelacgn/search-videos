import pytest
from django.test import Client


@pytest.mark.django_db
@pytest.mark.integration
class TestUserEndpoint:
    user_endpoint = '/api/user/'
    default_user_params =  {
        'email': 'test@test.com',
        'username': 'test',
        'first_name': 'test name',
        'last_name': 'test surname',
        'password': 'test1234',
        'password2': 'test1234'
    }

    @pytest.mark.parametrize(
        ('user_creation_params', 'status_code'),
        [
            (default_user_params, 201)
        ]
    )
    def test_user_creation_success(self, user_creation_params, status_code):
        response = Client().post(
            path=self.user_endpoint,
            data=user_creation_params
        )

        assert response.status_code == status_code

        response_json = response.json()
        assert 'id' in response_json
        response_json.pop('id')

        user_creation_params.pop('password')
        user_creation_params.pop('password2')

        assert response_json == user_creation_params


    @pytest.mark.parametrize(
        ('user_creation_params', 'test_field', 'status_code', 'error_msg'),
        [
            ({**default_user_params, 'email': ''}, 'email', 400, ['This field may not be blank.']),
            ({**default_user_params, 'username': ''}, 'username', 400, ['This field may not be blank.']),
            ({**default_user_params, 'first_name': ''}, 'first_name', 400, ['This field may not be blank.']),
            ({**default_user_params, 'last_name': ''}, 'last_name', 400, ['This field may not be blank.']),
            ({**default_user_params, 'password': ''}, 'password', 400, ['This field may not be blank.']),
            ({**default_user_params, 'password2': ''}, 'password2', 400, ['This field may not be blank.']),
            ({**default_user_params, 'email': 'test'}, 'email', 400, ['Enter a valid email address.']),
        ]
    )
    def test_user_creation_error(self, user_creation_params, test_field, status_code, error_msg):
        response = Client().post(
            path=self.user_endpoint,
            data=user_creation_params
        )

        assert response.status_code == status_code

        response_json = response.json()['detail']

        assert test_field in response_json
        assert response_json[test_field] == error_msg
