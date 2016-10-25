from django.shortcuts import render, redirect

from video.apis.youtube import youtube_search
__all__ = ['search']

def search(request):
    context = {}
    keyword = request.GET.get('keyword')
    page_token = request.GET.get('page_token')

    if keyword:
        response = youtube_search(keyword, page_token)
        context['keyword'] = keyword
        context['response'] = response
    return render(request, 'video/search.html', context)