import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from photo.models import Photo, PhotoLike, PhotoDislike

__all__ = [
    'photo_like',
]


@require_POST
@csrf_exempt
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
    is_delete = False
    # 좋아요가 이미 존재하는경우 좋아요 삭제
    if user_like_exist.exists():
        user_like_exist.delete()
        is_delete = True
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

    ret = {
        'like_count': photo.like_users.count(),
        'user_like': False,
    }
    if not is_delete:
        ret['user_like'] = True if like_type == 'like' else False

    return HttpResponse(json.dumps(ret), content_type='application/json')




