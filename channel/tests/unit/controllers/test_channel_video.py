from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock

from channel.controllers.channel_video import (
    retrieve_channel_videos,
    retrieve_single_video
)


class TestChannelVideoController(TestCase):
    @patch('channel.controllers.channel_video.VideoModel.objects.filter')
    def test_retrieve_all_videos_from_channel(self, mock_filter_videos):
        """ Test the flow of retrieving a range of videos.
        """
        user_id = 1234
        filter_results = MagicMock()
        mock_filter_videos.return_value = filter_results
        filter_results.sort.return_value = MagicMock()

        retrieve_channel_videos(user_id, offset=123, num_items=456)

        mock_filter_videos.assert_called_once_with(user=user_id)
        filter_results.order_by.assert_called_once_with('-published_date')

    @patch('channel.controllers.channel_video.VideoModel.objects.get')
    def test_retrieve_video_by_id(self, mock_get_video):
        """ Test the flow of retrieving a video by id.
        """
        video_id = 1234
        mock_get_video.return_value = Mock()

        retrieve_single_video(video_id)

        mock_get_video.assert_called_once_with(id=video_id)
