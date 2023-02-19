import datetime

from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    header = post.header
    preview = post.preview()
    section = post.section
    if section == 'NW':
        section = 'news'
    else:
        section = 'articles'
    subscribers_emails = []
    for category in categories:
        subscribers = category.subscribers.all()
        for user in subscribers:
            subscribers_emails.append(user.email)
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
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_dt__gte=last_week)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post_email.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }

    )
    msg = EmailMultiAlternatives(
        subject='Публикации за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
