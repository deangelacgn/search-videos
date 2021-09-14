from django_elasticsearch_dsl import (
    Document,
    fields,
)
from django_elasticsearch_dsl.registries import registry
from search.models.video import VideoModel
from django.conf import settings


@registry.register_document
class VideoDocument(Document):
    title = fields.TextField(
        attr='title',
        fields={
            'suggest': fields.Completion(),
        })
    transcript = fields.TextField(attr='transcript')
    description = fields.TextField(attr='description')
    user = fields.ObjectField(
        properties={
            'username': fields.TextField(),
            'id': fields.IntegerField(),
        })
    id = fields.IntegerField()
    url = fields.TextField()

    class Index:
        name = 'videos'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = VideoModel
        fields = ['published_date']
        related_models = [settings.AUTH_USER_MODEL]

    def prepare_id(self, instance):
        return instance.id

    def prepare_url(self, instance):
        return str(instance.url)

    def get_queryset(self):
        return super().get_queryset().select_related('user')

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, settings.AUTH_USER_MODEL):
            return related_instance.video_set.all()
