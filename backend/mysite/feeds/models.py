from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel


class Emotion(TimeStampedModel):
    """Define Emotion model."""
    # Create your models here.
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='feed_user',
        null=True,
        blank=True,
        editable=False,
        help_text='Feed of User')

    name = models.CharField(blank=True, null=True, max_length=100)


# Create your models here.
class Feed(TimeStampedModel):

    # Create your models here.
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='feed',
        null=True,
        blank=True,
        editable=False,
        help_text='Feed of User')
    content = models.CharField(max_length=255, blank=True)

    emotion = models.ManyToManyField(
        Emotion, related_name="emotion", null=True, blank=True)


class Comment(TimeStampedModel):
    # Create your models here.
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='comment_user',
        null=True,
        blank=True,
        editable=False,
        help_text='Comment of User')

    feed = models.ForeignKey(
        Feed,
        on_delete=models.SET_NULL,
        related_name='feed',
        null=True,
        blank=True,
        editable=False,
        help_text='comment for Feed')

    content = models.CharField(max_length=255, blank=True)
