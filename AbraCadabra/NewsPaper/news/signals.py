from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import PostCategory
from NewsPaper import settings


def send_notification(preview, pk, header, section, subscribers):
    if section == 'NW':
        section = 'news'
    else:
        section = 'articles'

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/{section}/{pk}',
            'header': header,
        }
    )

    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers_emails = []

        for category in categories:
            subscribers = category.subscribers.all()
            subscribers_emails += [sub.email for sub in subscribers]

        send_notification(instance.preview(), instance.pk, instance.header, instance.section, subscribers_emails)
