from django.core.mail import send_mail as django_send_mail
from django.conf import settings

__all__ = [
    'send_mail',
]

def send_test():
    django_send_mail(
        'subject',
        'message',
        settings.EMAIL_HOST_USER,
        ['openmind8735@gmail.com'],
        fail_silently=False,
    )


def send_mail(subject, message, recipient_list=None):
    default_recipient_list = ['openmind8735@gmail.com']
    django_send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list if recipient_list else default_recipient_list,
    )
