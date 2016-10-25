from django.shortcuts import render, redirect
from googleapiclient.discovery import build

from video.models import Video

DEVELOPER_KEY = "AIzaSyDeFsX6-gtB-iA_xslFF0OVDJfEqWk-Wb0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(keyword, page_token, max_results=5):
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
        )

    search_response = youtube.search().list(
        q=keyword,
        part="id,snippet",
        maxResults=max_results,
        pageToken=page_token,
    ).execute()


    video_id_list = []
    for item in search_response['items']:
        if item['id'].get('videoId'):
            cur_item = item['id']['videoId']
            video_id_list.append(cur_item)
    video_id = ','.join(video_id_list)

    video_response = youtube.videos().list(
        part="id,snippet,statistics,contentDetails",
        id=video_id,
    ).execute()

    for item in video_response['items']:
        cur_video_id = item['id']
        if Video.objects.filter(
                youtube_id=cur_video_id
        ).exists():
           item['is_exist'] = True

    # 다음페이지 버튼이 안나온다 어떻게 하지?

    try:
        video_response['nextPageToken'] = search_response['nextPageToken']
        video_response['prevPageToken'] = search_response['prevPageToken']
    except:
        pass
    return video_response