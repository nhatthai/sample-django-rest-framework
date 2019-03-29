from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
class Profile(TimeStampedModel):
    """Profile model of user."""

    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE
    )
    short_bio = models.CharField(
        null=True, blank=True, max_length=500
    )
    address = models.CharField(max_length=255, blank=True)
