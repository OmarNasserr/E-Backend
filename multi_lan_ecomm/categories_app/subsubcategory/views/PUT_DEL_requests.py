import json
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


from ..serializers import SubSubCategorySerializer
from ..validations import SubsubcategoryValidations
from ..subsubcategory_helper import Subsubcategories_Helper
from ..models import SubCategory,SubSubCategory
from helper_files.multi_languages import Multi_Languages_Support
from helper_files.permissions import IsAdminOrReadOnly,check_object_permissions,permission_denied
from helper_files.status_code import Status_code
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class SubSubCategoryDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubSubCategory.objects.all()
    serializer_class = SubSubCategorySerializer
    # permission_classes=[IsAdminOrReadOnly]
    
    def permission_denied(self, request):
        permission_denied(self=self ,request=request)
    
    def check_object_permissions(self, request, obj):
        check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            subsubcategory_id = aes.decrypt(str(self.kwargs['subsubcategory_id']))
            subsubcategory = SubSubCategory.objects.filter(pk=subsubcategory_id,)
            obj=subsubcategory[0]
        except:
            return ValueError('wrong id format')
        
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.subsubcategory.models.SubSubCategory'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(request.LANGUAGE_CODE),
                                  "status": Status_code.no_content},)
        response=Subsubcategories_Helper.subsubcategory_update(self, request,instance, *args, **kwargs)
            
        return response

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.subsubcategory.models.SubSubCategory'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(request.LANGUAGE_CODE),
                                  "status": Status_code.no_content},)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.subsubcategory.models.SubSubCategory'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(str(request.LANGUAGE_CODE)),
                                  "status": Status_code.no_content})
        return self.destroy(request,lang_code=request.LANGUAGE_CODE, *args, **kwargs)