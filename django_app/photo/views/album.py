from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from photo.forms import AlbumAdd
from photo.models import Album, Photo

__all__ = [
    'album_add',
    'album_detail',
    'album_list',
]


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'photo/album_list.html', {'albums': albums})


def album_add(request):
    # return HttpResponse('hello')
    if request.method == 'POST':
        form = AlbumAdd(request.POST)
        if form.is_valid():
            title = request.POST['title']
            owner = request.user
            description = request.POST['description']
            Album.objects.create(
                title=title,
                owner=owner,
                description=description,
            )
            return redirect('photo:album_list')
    else:
        form = AlbumAdd()

    return render(request, 'photo/album_add.html', {'form': form})


def album_detail(request, pk):
    album = Album.objects.get(pk=pk)
    photo_list = album.photo_set.all()
    paginator = Paginator(photo_list, 8)

    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)


    context = {
        'album': album,
        'photos': photos,
    }

    return render(request, 'photo/ajax_album_detail.html', context)