from django.urls import path
from channel.views.channel_video import ChannelVideoView

urlpatterns = [
    path('user/<int:user_id>/video/', ChannelVideoView.as_view()),
    path('user/<int:user_id>/video/<int:video_id>/', ChannelVideoView.as_view()),
]
