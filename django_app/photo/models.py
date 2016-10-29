from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models

from mysite.utils.models import BaseModel


class Album(BaseModel):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

class Photo(BaseModel):
    album = models.ForeignKey(Album)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    img = models.ImageField(upload_to='photo')
    img_thumbnail = models.ImageField(upload_to='photo/thumbnail', blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PhotoLike', related_name='photo_set_like_users')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PhotoDislike', related_name='photo_set_dislike_users')

    def __str__(self):
        return self.title

    # photo save override
    def save(self, *args, **kwargs):
        image_changed = False

        # 기존 이미지가 있는 경우
        if self.pk:
            original_photo = Photo.objects.get(pk=self.pk)
            if original_photo.img != self.img:
                image_changed = True

        # 기존 이미지가 없는 경우 신규등록
        if self.img and not self.img_thumbnail:
            image_changed = True

        # 조건이 충분한 경우 원본 이미지와 썸네일 저장
        super().save(*args, **kwargs)
        if image_changed:
            self.make_thumbnail()


    def make_thumbnail(self):
        import os
        from PIL import Image, ImageOps
        from io import BytesIO
        from django.core.files.storage import default_storage

        size = (300, 300)

        # 이미지의 경로를 가져옴
        f = default_storage.open(self.img)

        # 파일 Image 인스턴스화, file type 별도 저장
        image = Image.open(f)
        ftype = image.format

        # 리사이즈+크롭한 이미지를 저장
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # 기존파일 이름과 파일형식 추출
        # slpitext: 마지막 . 을 기준으로 slpit
        path, ext = os.path.splitext(self.img.name)
        name = os.path.basename(self.img.name)

        # 기존 파일 이름과 파일형식을 기반으로 thumbnail 이름 추출
        thumbnail_name = '%s_thumb%s' % (name, ext)

        # BytesIO로 임시 파일에 image 저장
        temp_file = BytesIO()
        image.save(temp_file, ftype)

        # read 위치 초기화
        temp_file.seek(0)

        # 임시파일과 썸네일 이름을 불러와서 썸네일 저장
        content_file = ContentFile(temp_file.read())
        self.img_thumbnail.save(thumbnail_name, content_file)

        # 모든 파일 종료
        temp_file.close()
        content_file.close()
        f.close()



class PhotoLike(BaseModel):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class PhotoDislike(BaseModel):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
