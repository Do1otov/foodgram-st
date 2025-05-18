from rest_framework.pagination import PageNumberPagination

from .constants import PAGINATION_DEFAULT_PAGE_SIZE, PAGINATION_MAX_PAGE_SIZE


class LimitPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGINATION_DEFAULT_PAGE_SIZE
    max_page_size = PAGINATION_MAX_PAGE_SIZE
