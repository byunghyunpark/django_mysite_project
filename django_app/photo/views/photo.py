from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from photo.forms import UploadFileForm
from photo.models import Album, Photo, PhotoLike, PhotoDislike

__all__ = [
    'upload_file',
    'photo_like',
    'photo_dislike',
]


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