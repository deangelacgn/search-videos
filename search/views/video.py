import logging

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from search.controllers.video import (
    retrieve_videos
)
from search.serializers.video import VideoSerializer
from drf_yasg.utils import swagger_auto_schema

class VideoView(APIView):
    permission_classes = (AllowAny,)
    logger = logging.getLogger(__name__)

    @swagger_auto_schema(responses={200: VideoSerializer})
    def get(self, request):
        try:
            search_query = request.query_params.get('search', None)
            offset = int(request.query_params.get('offset', 0))
            num_items = int(request.query_params.get('num_items', 9))

            videos = retrieve_videos(search_query, offset, num_items)
            return Response(videos, status=status.HTTP_200_OK)
        except Exception:
            self.logger.exception('Failed to retrieve video(s).')
            return Response(
                {'detail': 'Unable to retrieve videos. Please try again later.'},
                status=status.HTTP_400_BAD_REQUEST
            )
