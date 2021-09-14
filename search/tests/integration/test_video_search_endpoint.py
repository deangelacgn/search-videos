import pytest
from django.test import Client


@pytest.mark.django_db
@pytest.mark.integration
class TestVideoSearchEndpoint:
    video_endpoint = '/api/video/'

    @pytest.mark.parametrize(
        ('query_params', 'status_code', 'num_results'),
        [
            ({'offset': 0, 'num_items': 2}, 200, 2),
            ({'search': '', 'offset': 10, 'num_items': 20}, 200, 0)
        ]
    )
    def test_video_search_retrieval(self, query_params, status_code, num_results):
        response = Client().get(
            self.video_endpoint,
            query_params
        )

        assert response.status_code == status_code
        response_json = response.json()
        assert isinstance(response_json, list)
        assert len(response_json) == num_results
