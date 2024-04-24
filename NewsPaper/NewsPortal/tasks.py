import datetime
from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category

@shared_task
def new_post_send_email(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.headline
    subscribers_email = []
    for category in categories:
        subscribers__users = category.subscribers.all()
        for sub_user in subscribers__users:
            subscribers_email.append(sub_user.email)

    html_content = render_to_string(
                'html_email/news_created.html',
                {
                    'text': f'{post.text}',
                    'link': f'http://127.0.0.1:8000/news/{pk}'
                }
        )
    msg = EmailMultiAlternatives(
            subject = title,
            body = f'',
            from_email='andrey.astahow2016@yandex.ru',
            to = subscribers_email
        )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def news_post_last_week():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte = last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in = categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
                'html_email/news_last_week.html',
                {
                    'link': 'http://127.0.0.1:8000',
                    'posts': posts
                }
        )
    msg = EmailMultiAlternatives(
            subject = f'Привет! Вот новости за последнюю неделю:',
            body = f'',
            from_email='andrey.astahow2016@yandex.ru',
            to = subscribers
        )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

