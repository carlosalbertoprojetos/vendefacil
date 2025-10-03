"""
Custom pagination for VendaSimples project.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão para APIs"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page_size': self.get_page_size(self.request),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
        })


class LargeResultsSetPagination(PageNumberPagination):
    """Paginação para listas grandes"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
