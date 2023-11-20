from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import SubCategorySerializer
from ..models import Category,SubCategory
from ...pagination import CategoryAppPagination
from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)   


class SubCategoryList(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    
    pagination_class=CategoryAppPagination

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    filterset_fields=['languages__subcategory_name']
    search_fields = ['languages__subcategory_name']
    
    
    def get_queryset(self):
        category_id=aes.decrypt(str(self.kwargs['category_id']))
        return SubCategory.objects.filter(category=category_id)

    def get(self, request, *args, **kwargs):
        CategoryAppPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)