from audioop import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import exceptions, status

from ..serializers import ProductColorSerializer
from ..validations.product_color_validations import ProductColorValidations
from ..models import ProductColor
from helper_files.multi_languages import Multi_Languages_Support
from helper_files.status_code import Status_code
from helper_files.permissions import IsAdminOrReadOnly,permission_denied
from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)



class ProductColorCreate(generics.CreateAPIView):
    serializer_class=ProductColorSerializer     


    def create(self, request, *args, **kwargs):
        
        languages = Multi_Languages_Support.get_availabe_languages()
        lang_code = str(request.LANGUAGE_CODE)
        
        request.data._mutable=True
        try:
            request.data['product'] = int(aes.decrypt(
                str(request.data['product'])))
            request.data['color'] = int(aes.decrypt(
                str(request.data['color'])))
        except:
            pass
        
        
        serializer = self.get_serializer(data=request.data)
        valid,err=serializer.is_valid(raise_exception=False,languages=languages, used_language=lang_code)
        response = ProductColorValidations.check_product_color_create(self.request.data,
                                                                      valid,err,str(request.LANGUAGE_CODE))
        if response.status_code == Status_code.created:
            serializer.save()

        return response


