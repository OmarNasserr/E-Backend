from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import ProductColorSerializer
from ..models import ProductColor
from ..pagination import ProductAppPagination
from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)   


class ProductColorList(generics.ListAPIView):
    serializer_class = ProductColorSerializer
    queryset = ProductColor.objects.all()
    
    pagination_class=ProductAppPagination

    # filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    # filterset_fields=['languages__product_name']
    # search_fields = ['languages__product_name']
    
    def get_queryset(self):
        product_id=aes.decrypt(str(self.kwargs['product_id']))
        return ProductColor.objects.filter(product=product_id)
    
    def get(self, request, *args, **kwargs):
        ProductAppPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
    