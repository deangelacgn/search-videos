from django.urls import path
from search.views.video import VideoView


urlpatterns = [
    path('video/', VideoView.as_view()),
]
