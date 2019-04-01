# Define the paginations for resources
from rest_framework import pagination
from common import constants


class ProfilePagination(pagination.LimitOffsetPagination):
    default_limit = constants.PG_PROFILE_LIMIT
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = constants.PG_PROFILE_MAX
    template = 'rest_framework/pagination/numbers.html'
