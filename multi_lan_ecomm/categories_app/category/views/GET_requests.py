from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import CategorySerializer
from ..models import Category
from ...pagination import CategoryAppPagination
from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)   


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    pagination_class=CategoryAppPagination

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    filterset_fields=['languages__category_name']
    search_fields = ['languages__category_name']

    def get(self, request, *args, **kwargs):
        CategoryAppPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)