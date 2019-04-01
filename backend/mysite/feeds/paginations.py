# Define the paginations for resources
from common import constants
from common.paginations import CommonPagination


class FeedPagination(CommonPagination):
    default_limit = constants.PG_FEED_LIMIT
    max_limit = constants.PG_FEED_MAX
