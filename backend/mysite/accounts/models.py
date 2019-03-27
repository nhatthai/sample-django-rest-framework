from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel


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
