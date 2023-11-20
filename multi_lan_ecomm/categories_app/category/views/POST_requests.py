from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from helper_files.status_code import Status_code

from ..serializers import CategorySerializer
from ..validations import CategoryValidations
from helper_files.permissions import IsAdminOrReadOnly, permission_denied
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.multi_languages import Multi_Languages_Support

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class CategoryCreate(generics.CreateAPIView):
    # queryset=Product.objects.all()
    serializer_class = CategorySerializer

    # permission_classes=[IsAdminOrReadOnly]

    # def permission_denied(self, request):
    #     permission_denied(self=self ,request=request)

    def create(self, request, *args, **kwargs):
        
        #first we get the supported languages
        languages = Multi_Languages_Support.get_availabe_languages()
        #we get the language code that is sent in the request
        lang_code = str(request.LANGUAGE_CODE)

        #here we convert the body to json, because this field can be added from 'form-data' in postman
        #as we add it along with the image field, therefore we are making sure it's in json format
        request.data._mutable = True
        request.data['languages']=Multi_Languages_Support.convert_request_to_json(
            request=request,lang_code=lang_code
            )
        
        serializer = self.get_serializer(data=request.data)
        
        valid, err = serializer.is_valid(
            raise_exception=False, languages=languages, used_language=lang_code)
        
        response = CategoryValidations.check_category_create(
            request.data, valid, err, used_language=lang_code,languages=languages)
        
        if response.status_code == Status_code.created:
            serializer.save()
            response.data['item'] = serializer.data  # type: ignore

        return response