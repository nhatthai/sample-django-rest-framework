from django.http import Http404

from .models import Feed


def get_feed(feed_id):
    try:
        return Feed.objects.get(pk=feed_id)
    except Feed.DoesNotExist:
        raise Http404
