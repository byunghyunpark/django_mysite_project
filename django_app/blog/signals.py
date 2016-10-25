# from django.dispatch import receiver
# from django.db.models.signals import post_save
#
# from apis.mail import send_mail
# from blog.models import Comment
#
#
# # instance만 받아서 실행한다. save 오버라이드보다 깔끔하다
# @receiver(post_save, sender=Comment)
# def send_comment_mail(sender, instance, **kwargs):
#     title = '{} 글에 댓글이 달렸습니다'.format(instance.post.title)
#     content = '{} 에 {} 내용이 달렷네요'.format(
#         # datetime.strftime(format) : 입력된 포맷 형식에 맞추어 datetime 객체를 문자열로 반환
#         instance.created_date.strftime('%Y. %m. %d %H:%M'),
#         instance.content
#     )
#     print('send email')
#     send_mail(title, content)