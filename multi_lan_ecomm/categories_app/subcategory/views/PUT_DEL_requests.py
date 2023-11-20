import json
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


from ..serializers import SubCategorySerializer
from ..validations import SubcategoryValidations
from ..subcategory_helper import Subcategory_Helper
from ..models import SubCategory
from helper_files.multi_languages import Multi_Languages_Support
from helper_files.permissions import IsAdminOrReadOnly,check_object_permissions,permission_denied
from helper_files.status_code import Status_code
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class SubCategoryDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    # permission_classes=[IsAdminOrReadOnly]
    
    def permission_denied(self, request):
        permission_denied(self=self ,request=request)
    
    def check_object_permissions(self, request, obj):
        check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            subcategory_id = aes.decrypt(str(self.kwargs['subcategory_id']))
            subcategory = SubCategory.objects.filter(pk=subcategory_id,)
            obj=subcategory[0]
        except:
            return ValueError('wrong id format')
        
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.subcategory.models.SubCategory'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(request.LANGUAGE_CODE),
                                  "status": Status_code.no_content},)
        response=Subcategory_Helper.subcategory_update(self, request,instance, *args, **kwargs)
            
        return response
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.subcategory.models.SubCategory'>":
            return Response(data={"message": "Subcategory wasn't found.",
                                  "status": Status_code.no_content})
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.subcategory.models.SubCategory'>":
            return Response(data={"message": "Subcategory wasn't found.",
                                  "status": Status_code.no_content})
    
        return self.destroy(request,lang_code=request.LANGUAGE_CODE, *args, **kwargs)