from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import UserSerializer
from django.contrib.auth.models import User
from ..pagination import UsersPagination


class UsersList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    pagination_class=UsersPagination  

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    filterset_fields=['username','is_staff','is_superuser',]
    search_fields = ['username','is_staff','is_superuser',]
    
    def get(self, request, *args, **kwargs):
        UsersPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
    