from audioop import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import exceptions, status

from ..serializers import ProductSerializer
from ..validations.validations import ProductValidations
from ..models import Product
from helper_files.multi_languages import Multi_Languages_Support
from helper_files.status_code import Status_code
from helper_files.permissions import IsAdminOrReadOnly,permission_denied
from django.conf import settings
from helper_files.cryptography import AESCipher
from parler.views import TranslatableCreateView

aes = AESCipher(settings.SECRET_KEY[:16], 32)



class ProductCreate(generics.CreateAPIView):
    serializer_class=ProductSerializer     


    def create(self, request, *args, **kwargs):
        
        languages = Multi_Languages_Support.get_availabe_languages()
        lang_code = str(request.LANGUAGE_CODE)

        request.data._mutable = True
        request.data['languages']=Multi_Languages_Support.convert_request_to_json(
            request=request,lang_code=lang_code
            )
        request.data['subsubcategory'] = int(aes.decrypt(
            str(request.data['subsubcategory'])))
        
        serializer = self.get_serializer(data=request.data)
        
        valid, err = serializer.is_valid(raise_exception=False, languages=languages, used_language=lang_code)
        
        response = ProductValidations.check_product_create(
            request.data, valid, err,lang_code,languages)
        
        if response.status_code == Status_code.created:
            serializer.save()
            response.data['item'] = serializer.data  # type: ignore

        return response


