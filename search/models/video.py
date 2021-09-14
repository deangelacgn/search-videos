from django.db import models
from django.conf import settings


class VideoModel(models.Model):
    title = models.CharField(max_length=500, blank=True)
    transcript = models.TextField(blank=True)
    url = models.URLField(max_length=500, blank=True)
    description = models.TextField(default='', blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
