from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save

from apis.mail import send_mail
from apis.sms import send_sms


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     # 먼저 save를 진행하고 그 아래 동작을 수행한다
    #     super(Comment, self).save(*args, **kwargs)
    #     recipient_list = [self.post.author.email]
    #     title = '{} 글에 댓글이 달렸습니다'.format(self.post.title)
    #     content = '{} 에 {} 내용이 달렷네요'.format(
    #         # datetime.strftime(format) : 입력된 포맷 형식에 맞추어 datetime 객체를 문자열로 반환
    #         self.created_date.strftime('%Y. %m. %d %H:%M'),
    #         self.content
    #     )
    #     send_mail(title, content, recipient_list)


def send_comment_reaction(sender, instance, **kwargs):
    """
    save 오버라이드 안하고 signal 사용
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    title = '{} 글에 댓글이 달렸습니다'.format(instance.post.title)
    content = '{} 에 {} 내용이 달렷네요'.format(
        # datetime.strftime(format) : 입력된 포맷 형식에 맞추어 datetime 객체를 문자열로 반환
        instance.created_date.strftime('%Y. %m. %d %H:%M'),
        instance.content
    )
    send_mail(title, content)
    receiver_number = instance.post.author.phone_number
    send_sms(title, receiver_number)

post_save.connect(send_comment_reaction, sender=Comment)



"""

# instance만 받아서 실행한다. save 오버라이드보다 깔끔하다
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Comment)
def send_comment_mail(sender, instance, **kwargs):
    title = '{} 글에 댓글이 달렸습니다'.format(instance.post.title)
    content = '{} 에 {} 내용이 달렷네요'.format(
        # datetime.strftime(format) : 입력된 포맷 형식에 맞추어 datetime 객체를 문자열로 반환
        instance.created_date.strftime('%Y. %m. %d %H:%M'),
        instance.content
    )
    send_mail(title, content)

"""