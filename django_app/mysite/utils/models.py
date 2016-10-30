from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modifed_date = models.DateTimeField(auto_now=True)

    # 가상화해준다
    class Meta:
        abstract = True

    def url_field(self, fieldname, default=''):
        # fieldname 이라는 속성을 찾아서 출력한다
        field = getattr(self, fieldname)

        if field and hasattr(field, 'url'):
            return field.url
        return default

