from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Post, Response
from MMOBulletinBoard import settings


def send_notification(email, text, header, flag):

    if flag == 'new':
        html_content = render_to_string(
            'response_new_email.html',
            {
                'text': text,
                'link': f'{settings.SITE_URL}/responses',
                'header': header,
            }
        )
    elif flag == 'deny':
        html_content = render_to_string(
            'response_deny_email.html',
            {
                'text': text,
                'link': f'{settings.SITE_URL}/posts',
                'header': header,
            }
        )

    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Response)
def notify_user_new_response(sender, instance, created, **kwargs):
    if created:
        email = []
        email += [instance.post.sender.email]
        text = instance.text
        header = instance.post.header
        flag = 'new'

        send_notification(email, text, header, flag)


@receiver(post_delete, sender=Response)
def notify_user_deny_response(sender, instance, **kwargs):
    email = []
    email += [instance.sender.email]
    text = instance.text
    header = instance.post.header
    flag = 'deny'

    send_notification(email, text, header, flag)
