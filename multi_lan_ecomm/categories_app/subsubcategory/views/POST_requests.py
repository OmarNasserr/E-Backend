from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from helper_files.status_code import Status_code

from ..serializers import SubSubCategorySerializer
from ..validations import SubsubcategoryValidations
from ..models import SubCategory
from helper_files.permissions import IsAdminOrReadOnly, permission_denied
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.multi_languages import Multi_Languages_Support

aes = AESCipher(settings.SECRET_KEY[:16], 32)




class SubSubCategoryCreate(generics.CreateAPIView):
    # queryset=Product.objects.all()__vsclatawkow
    serializer_class = SubSubCategorySerializer
    # permission_classes=[IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        
        languages = Multi_Languages_Support.get_availabe_languages()
        lang_code = str(request.LANGUAGE_CODE)

        request.data._mutable = True
        request.data['languages']=Multi_Languages_Support.convert_request_to_json(
            request=request,lang_code=lang_code
            )
        
        try:
            request.data['subcategory'] = int(aes.decrypt(
                str(request.data['subcategory'])))
        except: 
            message = Multi_Languages_Support.return_err_message(
                                used_language=lang_code,
                                msgEN="subcategory field is missing.",
                                msgAR="حقل subcategory مفقود"
                            )
            return Response(data={"message": message, "status": Status_code.created},
                            status=Status_code.updated)

        serializer = self.get_serializer(data=request.data)
        
        valid, err = serializer.is_valid(raise_exception=False, languages=languages, used_language=lang_code)
        
        response = SubsubcategoryValidations.check_sub_sub_category_create(
            request.data, valid, err,lang_code,languages)
        
        if response.status_code == Status_code.created:
            serializer.save()
            response.data['item'] = serializer.data  # type: ignore

        return response