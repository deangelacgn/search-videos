from search.models.video import VideoModel
from django.db.models.query import QuerySet


def publish_video(user_id: int, video_info: dict) -> VideoModel:
    """ 
    Add a new video in the database.
    """
    video_info['user_id'] = user_id
    video_instance = VideoModel.objects.create(**video_info)
    return video_instance


def update_video_details(video: VideoModel, details: dict) -> None:
    """
    Update the fields of a video object in the database.
    """
    for attr, value in details.items():
        setattr(video, attr, value)
    video.save()


def remove_video(video: VideoModel) -> None:
    """
    Delete a video from the database.
    """
    video.delete()


def retrieve_channel_videos(user_id: int, offset: int, num_items: int) -> QuerySet:
    """
    Retrieve all videos published by an user from the database.
    """
    videos = VideoModel.objects.filter(user=user_id).order_by('-published_date')
    videos = videos[offset:offset+num_items]
    return videos


def retrieve_single_video(video_id: int) -> VideoModel:
    """
    Retrieve a single video from the database.
    """
    video = VideoModel.objects.get(id=video_id)
    return video
