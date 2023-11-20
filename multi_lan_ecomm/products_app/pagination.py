from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response
from rest_framework import status



class ProductAppPagination(PageNumberPagination):
    page_size=1
    page_query_param='page_number' #defines the name of /?page_number=, default is page
    page_size_query_param='page_size' #gives the user the ability to controll the number of 
                                 #items returned
    max_page_size=10 #controls max number a user can return, therefore page_size_query_param max value = 10
    last_page_strings='last page'
    def get_paginated_response(self, data):
        status_returned=status.HTTP_200_OK
        message=''
        if len(data)==0:
            status_returned=status.HTTP_204_NO_CONTENT
        return Response({
            'status':status_returned,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_number_of_objects': self.page.paginator.count,
            'number_of_pages': self.page.paginator.num_pages,
            'current_page':self.page.number,
            'last_page': self.page.paginator.count,
            'count_items_in_page': self.page_size,
            'results': data,
            
        })
        
    #in case page_number or page_size wasn't declared in the url params
    #this sets a default value that insures that the request is delivered safely
    def set_default_page_number_and_page_size(request):
        if 'page_size' in request.GET:
            pass
        else:
            request.GET._mutable = True
            request.GET['page_size'] = 5
        if 'page_number' in request.GET:
            pass
        else:
            request.GET._mutable = True
            request.GET['page_number'] = '1'