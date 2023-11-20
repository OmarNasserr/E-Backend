from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import SubSubCategorySerializer
from ..models import SubSubCategory
from ...pagination import CategoryAppPagination
from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)   


class SubSubCategoryList(generics.ListAPIView):
    serializer_class = SubSubCategorySerializer
    queryset = SubSubCategory.objects.all()
    
    pagination_class=CategoryAppPagination

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    filterset_fields=['languages__subsubcategory_name']
    search_fields = ['languages__subsubcategory_name']
    
    def get_queryset(self):
        subcategory_id=aes.decrypt(str(self.kwargs['subcategory_id']))
        return SubSubCategory.objects.filter(subcategory=subcategory_id)
    
    def get(self, request, *args, **kwargs):
        CategoryAppPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)