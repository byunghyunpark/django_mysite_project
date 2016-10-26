from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^album/list/$', views.album_list, name='album_list'),
    url(r'album/add/$', views.album_add, name='album_add'),
]