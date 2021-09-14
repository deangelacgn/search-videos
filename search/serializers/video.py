from rest_framework import serializers
from search.models.video import VideoModel


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = '__all__'

    def validate_url(self, value):
        if self.instance and self.instance.url != value:
            raise serializers.ValidationError("This field cannot be edited.")
        return value
