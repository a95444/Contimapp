from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, File
from django.db.models.signals import pre_save
from django.conf import settings
import os

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(pre_save, sender=File)
def ensure_user_folder_exists(sender, instance, **kwargs):
    if instance.created_by:
        user_folder = os.path.join(settings.MEDIA_ROOT, f'files_user{instance.created_by.id}')
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)