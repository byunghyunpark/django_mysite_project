from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404

from photo.forms import UploadFileForm, UploadMultiFileForm
from photo.models import Album, Photo, PhotoLike, PhotoDislike

__all__ = [
    'upload_file',
    'photo_like',
    'upload_multi_file',
]


@login_required
def upload_file(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
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
            return redirect('photo:album_detail', pk=album_pk)
    else:
        form = UploadFileForm()
    return render(request, 'photo/upload.html', {'form': form})


@login_required
@require_POST
def photo_like(request, pk, like_type='like'):

    photo = get_object_or_404(Photo, pk=pk)
    album = photo.album
    user = request.user
    like_model = PhotoLike if like_type == 'like' else PhotoDislike
    opposite_model = PhotoDislike if like_type == 'like' else PhotoLike

    user_like_exist = like_model.objects.filter(
        user=user,
        photo=photo,
    )
    # 좋아요가 이미 존재하는경우 좋아요 삭제
    if user_like_exist.exists():
        user_like_exist.delete()
    # 좋아요 생성
    else:
        like_model.objects.create(
            user=user,
            photo=photo,
        )
        # 만약 싫어요 클릭되있는 경우 싫어요 삭제
        opposite_model.objects.filter(
            user=user,
            photo=photo,
        ).delete()

    return redirect('photo:album_detail', pk=album.pk)


@login_required
def upload_multi_file(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == 'POST':
        form = UploadMultiFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            owner = request.user
            description = form.cleaned_data['description']

            # file을 list로 받는다
            files = request.FILES.getlist('file')

            # i 인덱스를 매겨서 files 리스트를 튜플로 출력
            for i, file in enumerate(files):
                Photo.objects.create(
                    album=album,
                    owner=owner,
                    title='%s(%s)' % (title, i+1),
                    description='%s(%s)' % (description, i+1),
                    img=file,
            )
            return redirect('photo:album_detail', pk=album_pk)
    else:
        form = UploadMultiFileForm()
    return render(request, 'photo/multi_upload.html', {'form': form})


