from django.conf import settings
from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        self.title

class Photo(models.Model):
    Album = models.ForeignKey(Album)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    img = models.ImageField(upload_to='photo')

    def __str__(self):
        self.title

