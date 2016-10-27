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
    photos = Photo.objects.filter(album=pk)
    album = Album.objects.get(pk=pk)
    context = {
        'photos': photos,
        'pk': pk,
        'album': album,
    }
    return render(request, 'photo/album_detail.html', context)