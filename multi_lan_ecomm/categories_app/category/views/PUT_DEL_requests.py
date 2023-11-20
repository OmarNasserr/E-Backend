import json
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


from ..serializers import CategorySerializer
from ..validations import CategoryValidations
from ..category_helper import Category_Helper
from ..models import Category
from helper_files.multi_languages import Multi_Languages_Support
from helper_files.permissions import IsAdminOrReadOnly,check_object_permissions,permission_denied
from helper_files.status_code import Status_code
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class CategoryDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes=[IsAdminOrReadOnly]
    
    def permission_denied(self, request):
        permission_denied(self=self ,request=request)
    
    def check_object_permissions(self, request, obj):
        check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            category_id = aes.decrypt(str(self.kwargs['category_id']))
            category = Category.objects.filter(pk=int(category_id))
            obj=category[0]
            print("OBBBJ ",type(obj))
        except:
            return ValueError('wrong id format')

        if category.count() == 0:
            return ValueError('wrong id format')
        
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.category.models.Category'>":
            return Response(data={"message": "Category wasn't found.",
                                  "status": Status_code.no_content})
        
        response=Category_Helper.category_update(self, request,instance, *args, **kwargs)
            
        return response


    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.category.models.Category'>":
            return Response(data={"message": "Category wasn't found.",
                                  "status": Status_code.no_content})
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'categories_app.category.models.Category'>":
            return Response(data={"message": "Category wasn't found.",
                                  "status": Status_code.no_content})
    
        return self.destroy(request,lang_code=request.LANGUAGE_CODE, *args, **kwargs)