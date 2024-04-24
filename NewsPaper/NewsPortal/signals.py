from django.core.mail import send_mail, EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.template.loader import render_to_string

from .models import PostCategory
from .tasks import new_post_send_email

@receiver(m2m_changed, sender=PostCategory)
def post_send_mail(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_send_email(instance.pk)