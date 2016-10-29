from django.conf.urls import url

from photo import ajax
from . import views

urlpatterns = [
    url(r'^album/list/$', views.album_list, name='album_list'),
    url(r'album/add/$', views.album_add, name='album_add'),
    url(r'album/(?P<pk>[0-9]+)/$', views.album_detail, name='album_detail'),
    url(r'album/upload/(?P<album_pk>[0-9]+)/$', views.upload_file, name='upload'),
    url(r'album/multiupload/(?P<album_pk>[0-9]+)/$', views.upload_multi_file, name='upload_multi'),
    url(r'album/photo/(?P<pk>[0-9]+)/(?P<like_type>\w+)/$', views.photo_like, name='photo_like'),
    url(r'^ajax/photo/(?P<pk>[0-9]+)/(?P<like_type>\w+)/$', ajax.photo_like, name='ajax_photo_like'),
]