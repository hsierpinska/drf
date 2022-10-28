from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=255)
    album_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=255)  # dominant color
    url = models.CharField(max_length=255)
# Create your models here.
# ID, title, album ID, width, height, color (dominant color), URL (URL to
# locally stored file)
