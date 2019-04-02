from django.shortcuts import get_object_or_404

from .models import Feed


def get_feed(feed_id):
    return get_object_or_404(Feed, id=feed_id)
