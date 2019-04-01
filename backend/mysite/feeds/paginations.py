# Define the paginations for resources
from commons import constants
from commons.paginations import CommonPagination


class FeedPagination(CommonPagination):
    default_limit = constants.PG_FEED_LIMIT
    max_limit = constants.PG_FEED_MAX
