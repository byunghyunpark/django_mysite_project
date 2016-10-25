# from django.shortcuts import render, redirect
#
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from oauth2client.tools import argparser
#
# from video.models import Video
#
# DEVELOPER_KEY = "AIzaSyDeFsX6-gtB-iA_xslFF0OVDJfEqWk-Wb0"
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"
#
#
# def youtube_search(keyword, page_token, max_results=10):
#   youtube = build(
#       YOUTUBE_API_SERVICE_NAME,
#       YOUTUBE_API_VERSION,
#       developerKey=DEVELOPER_KEY
#   )
#
#   search_response = youtube.search().list(
#     q=keyword,
#     part="id,snippet",
#     maxResults=max_results,
#     pageToken=page_token,
#   ).execute()
#
#   return search_response
#
#
# def search(request):
#     context = {}
#     keyword = request.GET.get('keyword')
#     page_token = request.GET.get('page_token')
#
#     if keyword:
#         response = youtube_search(keyword, page_token)
#         context['keyword'] = keyword
#         context['response'] = response
#     return render(request, 'video/search.html', context)
#
#
# def add_bookmark(request):
#
#     if request.method == "POST":
#         kind = request.POST.get
#         video = Video(
#             kind = request.POST['kind'],
#             videoId = request.POST['videoId'],
#             title= request.POST['title'],
#             description = request.POST['description'],
#             publishedAt = request.POST['publishedAt'],
#             thumbnails = request.POST['thumbnails'],
#         )
#         video.save()
#         return redirect('video:search')
#
#     else:
#         pass
#
#
# def bookmark_list(request):
#     videos = Video.objects.all()
#     return render(request, 'video/bookmark_list.html', {'videos': videos})