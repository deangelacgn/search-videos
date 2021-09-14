import pytest
from django.test import Client
import time


@pytest.mark.django_db
@pytest.mark.integration
class TestChannelVideoEndpoint:

    @pytest.mark.parametrize(
        ('video_data', 'status_code'),
        [
            ({
                'url': 'https://www.youtube.com/watch?v=Wx1B5GJb_to',
                'description': 'test',
                'transcript': 'test abcd',
                'title': 'test title'
            },
                201,
            ),
        ]
    )
    def test_publish_video(self, video_data, status_code):
        user_id, access_token = self.get_user_access()

        video_data = {
            'url': 'https://www.youtube.com/watch?v=Wx1B5GJb_to',
            'description': 'test',
            'transcript': 'test abcd',
            'title': 'test title',
        }

        response = Client().post(
            f'/api/user/{user_id}/video/',
            video_data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        assert response.status_code == status_code

        response_json = response.json()
        assert 'id' in response_json
        assert 'user' in response_json
        assert 'published_date' in response_json
        
        for attr, value in video_data.items():
            assert response_json[attr] == value

    @staticmethod
    def get_user_access():
        test_user = {
                'first_name': 'test name',
                'last_name': 'test surname',
                'email': f'{time.time()}@test.com',
                'username': time.time(),
                'password': 'test1234',
                'password2': 'test1234'
            }
        
        signup_response = Client().post(
            path='/api/user/',
            data=test_user
        )

        response = Client().post(
            path='/api/login/',
            data={
                'username': test_user['username'],
                'password': test_user['password']
            }
        )

        login_response = response.json()
        user_id = login_response['user']['id']
        access_token = login_response['access']

        return user_id, access_token
