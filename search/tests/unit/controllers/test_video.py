from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
from search.controllers.video import retrieve_videos


class TestVideoController(TestCase):
    @patch('search.controllers.video.VideoDocument')
    @patch('search.controllers.video.MultiMatch')
    @patch('search.controllers.video.MatchAll')
    def test_video_retrieval__search_all(self, match_all_mock, multi_match_mock, video_doc_mock):
        """ Test the flow of retrieving a range of videos.
        """
        query = Mock()
        search = MagicMock()
        response = MagicMock()

        search.execute.return_value = response
        response.to_dict.return_value = {
            'hits': {
                'hits': [
                    {
                        'id': 123,
                        'transcript': 'test',
                        'content': 'test',
                        'title': 'test',
                    }
                ]
            }
        }

        match_all_mock.return_value = query
        multi_match_mock.return_value = query
        video_search_query = video_doc_mock.search.return_value.query
        video_search_query.return_value = search

        retrieve_videos(None, 0, 12)

        match_all_mock.assert_called_once_with()
        multi_match_mock.assert_not_called()
        video_search_query.assert_called_once_with(query)

    @patch('search.controllers.video.VideoDocument')
    @patch('search.controllers.video.MultiMatch')
    @patch('search.controllers.video.MatchAll')
    def test_video_retrieval__search_related_videos(self, match_all_mock, multi_match_mock, video_doc_mock):
        """ Test the flow of searching videos related to a given text query
        """
        query = Mock()
        search = MagicMock()
        response = MagicMock()

        fields_to_search = ['title', 'transcript', 'description']

        search.execute.return_value = response
        response.to_dict.return_value = {
            'hits': {
                'hits': [
                    {
                        'id': 123,
                        'transcript': 'test',
                        'content': 'test',
                        'title': 'test',
                    }
                ]
            }
        }

        match_all_mock.return_value = query
        multi_match_mock.return_value = query
        video_search_query = video_doc_mock.search.return_value.query
        video_search_query.return_value = search

        retrieve_videos('test', 0, 12)

        match_all_mock.assert_not_called()
        multi_match_mock.assert_called_once_with(
            query='test',
            fields=fields_to_search,
            fuzziness='AUTO'
        )
        video_search_query.assert_called_once_with(query)
