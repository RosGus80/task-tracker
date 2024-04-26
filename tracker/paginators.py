from rest_framework.pagination import PageNumberPagination


class BasePaginator(PageNumberPagination):
    """Пагинатор для списков сотрудников и задач"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
