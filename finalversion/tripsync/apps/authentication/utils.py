from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(to_email, body):
    send_mail(
        subject='Verify your email',
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )