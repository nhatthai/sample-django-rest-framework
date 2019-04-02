# Define the paginations for resources
from rest_framework import pagination


class CommonPagination(pagination.LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100
    template = 'rest_framework/pagination/numbers.html'
