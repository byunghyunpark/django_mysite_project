from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import AlbumAdd, UploadFileForm
from photo.models import Album, Photo, PhotoLike, PhotoDislike


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



# from somewhere import handle_uploaded_file
@login_required
def upload_file(request, pk):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            album = Album.objects.get(pk=pk)
            title = form.cleaned_data['title']
            owner = request.user
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']
            Photo.objects.create(
                album=album,
                owner=owner,
                title=title,
                description=description,
                img=file,
            )
            return redirect('photo:album_detail', pk=pk)
    else:
        form = UploadFileForm()
    return render(request, 'photo/upload.html', {'form': form})


def photo_like(request, pk):
    next = request.GET.get('next')
    if request.method == 'POST':
        photo = Photo.objects.get(pk=pk)
        album_pk = photo.album.pk
        user = request.user
        if PhotoLike.objects.filter(user=user, photo=photo).exists():
            PhotoLike.objects.get(user=user, photo=photo).delete()
        else:
            PhotoLike.objects.create(
                photo=photo,
                user=user,
            )
        return redirect('photo:album_detail', pk=album_pk)
    else:
        return redirect(next)

def photo_dislike(request, pk):
    next = request.GET.get('next')
    if request.method == 'POST':
        photo = Photo.objects.get(pk=pk)
        album_pk = photo.album.pk
        user = request.user
        if PhotoDislike.objects.filter(user=user, photo=photo).exists():
            PhotoDislike.objects.get(user=user, photo=photo).delete()
        else:
            PhotoDislike.objects.create(
                photo=photo,
                user=user,
            )
        return redirect('photo:album_detail', pk=album_pk)
    else:
        return redirect(next)