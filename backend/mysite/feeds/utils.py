from .models import Feed


def get_feed(feed_id):
    """
    Get Feed by id
    """
    return Feed.objects.get_feed(feed_id)[0]
