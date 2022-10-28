from .models import Photo
from rest_framework import serializers


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'album_id', 'width', 'height', 'color', 'url']
