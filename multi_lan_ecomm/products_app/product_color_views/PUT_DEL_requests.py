from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from products_app.product_helper import Product_Helper
from helper_files.multi_languages import Multi_Languages_Support
from helper_files.status_code import Status_code


from ..serializers import ProductColorSerializer
from ..validations.product_color_validations import ProductColorValidations
from ..models import ProductColor, ProductVariations
from helper_files.permissions import IsAdminOrReadOnly,check_object_permissions,permission_denied
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)

class ProductColorDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer
    # permission_classes=[IsAdminOrReadOnly]
    
    # def permission_denied(self, request):
    #     permission_denied(self=self ,request=request)
    
    # def check_object_permissions(self, request, obj):
    #     check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            product_color_id = aes.decrypt(str(self.kwargs['product_color_id']))
            product_color = ProductColor.objects.filter(pk=product_color_id,)
            obj=product_color[0]
        except:
            return ValueError('wrong id format')
        
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        languages = Multi_Languages_Support.get_availabe_languages()
        lang_code = str(request.LANGUAGE_CODE)
        instance = self.get_object()
        if str(type(instance)) != "<class 'products_app.models.ProductColor'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(request.LANGUAGE_CODE),
                                  "status": Status_code.no_content},)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            valid,err=serializer.is_valid(raise_exception=True,languages=languages, used_language=lang_code)
            response=ProductColorValidations.check_product_color_update(self.request.data,valid,err,str(request.LANGUAGE_CODE))
            if response.status_code == Status_code.updated:
                serializer.save()
                response.data['color']=serializer.data

            return response

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'products_app.models.ProductColor'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(request.LANGUAGE_CODE),
                                  "status": Status_code.no_content},)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'products_app.models.ProductColor'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(str(request.LANGUAGE_CODE)),
                                  "status": Status_code.no_content})
        product_variations=ProductVariations.objects.filter(product_color_variations=instance.id)
        for variation in product_variations:
            variation.delete()
        return self.destroy(request,lang_code=request.LANGUAGE_CODE, *args, **kwargs)