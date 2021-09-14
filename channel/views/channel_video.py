import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from search.models.video import VideoModel

from account.permissions.video_access import VideoAccessPermision
from search.serializers.video import VideoSerializer

from channel.controllers.channel_video import (
    publish_video,
    retrieve_channel_videos,
    retrieve_single_video,
    update_video_details,
    remove_video
)
from drf_yasg.utils import swagger_auto_schema

class ChannelVideoView(APIView):
    permission_classes = (VideoAccessPermision,)
    logger = logging.getLogger(__name__)

    @swagger_auto_schema(
        operation_description='Retrieve videos from a user channel.',
        responses={200: VideoSerializer})
    def get(self, request, user_id, video_id=None):
        try:
            if video_id is None:
                offset = int(request.query_params.get('offset', 0))
                num_items = int(request.query_params.get('num_items', 9))
                videos = retrieve_channel_videos(user_id, offset, num_items)
                videos = [VideoSerializer(video).data for video in videos]
                return Response(videos, status=status.HTTP_200_OK)
            video = retrieve_single_video(video_id)
            video = VideoSerializer(video).data
            return Response(video, status=status.HTTP_200_OK)
        except VideoModel.DoesNotExist:
            self.logger.exception(f'Video {video_id} not found.')
            return Response({'detail': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception('Failed to retrieve channel video(s).')
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="Publish a video in the user's channel.",
        responses={201: VideoSerializer})
    def post(self, request, user_id):
        try:
            serializer = VideoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            video_instance = publish_video(request.user.id, serializer.validated_data)
            video = VideoSerializer(video_instance).data
            return Response(video, status=status.HTTP_201_CREATED)
        except ValidationError:
            self.logger.exception('Found invalid fields while publishing videos.')
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            self.logger.exception('Failed to publish video.')
            return Response({'detail': 'Something went wrong. Please try again later.'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update the properties of a video published in a user's channel.",
        responses={204: ''})
    def patch(self, request, user_id, video_id):
        try:
            video = retrieve_single_video(video_id)
            self.check_object_permissions(request, video)
            serializer = VideoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            update_video_details(video, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError:
            self.logger.exception('Found invalid fields while editing video {id}.')
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except VideoModel.DoesNotExist:
            self.logger.exception('Video {id} does not exist.')
            return Response({'detail': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            self.logger.exception(f'User {request.user.id} does not have permission to update video {id}.')
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            self.logger.exception('Failed to update video {id}.')
            return Response({'detail': 'Something went wrong. Please try again later.'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete video(s) from a user's channel.",
        responses={200: 'Message indicating whether the operation has succeeded or not.'})
    def delete(self, request, user_id, video_id):
        try:
            video = retrieve_single_video(video_id)
            self.check_object_permissions(request, video)
            remove_video(video)
            return Response({'detail': 'Video has been successfully removed.'}, status=status.HTTP_200_OK)
        except PermissionDenied:
            self.logger.exception(f'User {request.user.id} does not have permission to delete video {id}.')
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        except VideoModel.DoesNotExist:
            self.logger.exception('Video {id} does not exist.')
            return Response({'detail': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception('Failed to remove video {id}.')
            return Response({'detail': 'Something went wrong. Please try again later.'}, status=status.HTTP_400_BAD_REQUEST)
