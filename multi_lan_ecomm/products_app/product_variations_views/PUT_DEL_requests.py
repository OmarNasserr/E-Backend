from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from products_app.product_helper import Product_Helper
from helper_files.multi_languages import Multi_Languages_Support
from helper_files.status_code import Status_code
from products_app.validations.product_variation_validations import ProductVariationValidations


from ..serializers import ProductVariationsSerializer
from ..validations.product_color_validations import ProductColorValidations
from ..models import ProductVariations
from helper_files.permissions import IsAdminOrReadOnly,check_object_permissions,permission_denied
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)

class ProductVariationDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariations.objects.all()
    serializer_class = ProductVariationsSerializer
    # permission_classes=[IsAdminOrReadOnly]
    
    # def permission_denied(self, request):
    #     permission_denied(self=self ,request=request)
    
    # def check_object_permissions(self, request, obj):
    #     check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            product_var_id = aes.decrypt(str(self.kwargs['product_varaition_id']))
            product_var = ProductVariations.objects.filter(pk=product_var_id,)
            obj=product_var[0]
        except:
            return ValueError('wrong id format')
        
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        languages = Multi_Languages_Support.get_availabe_languages()
        lang_code = str(request.LANGUAGE_CODE)
        instance = self.get_object()
        if str(type(instance)) != "<class 'products_app.models.ProductVariations'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(request.LANGUAGE_CODE),
                                  "status": Status_code.no_content},)
        else:
            request.data._mutable=True
            if 'product' in request.data.keys():
                request.data['product'] = int(aes.decrypt(
                    str(request.data['product'])))
            if 'product_color_variations' in request.data.keys():
                request.data['product_color_variations'] = int(aes.decrypt(
                    str(request.data['product_color_variations'])))
            if 'size' in request.data.keys():
                request.data['size'] = int(aes.decrypt(
                    str(request.data['size'])))
            if 'number_in_stock' in request.data.keys():
                request.data['number_in_stock'] = int(str(request.data['number_in_stock']))
            
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            valid,err=serializer.is_valid(raise_exception=True,languages=languages, used_language=lang_code)
            response=ProductVariationValidations.check_product_variation_update(self.request.data,valid,err,str(request.LANGUAGE_CODE))
            if response.status_code == Status_code.updated:
                serializer.save()
                response.data['product_variation']=serializer.data

            return response

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'products_app.models.ProductVariations'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(request.LANGUAGE_CODE),
                                  "status": Status_code.no_content},)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'products_app.models.ProductVariations'>":
            return Response(data={"message": Multi_Languages_Support.not_found_message(str(request.LANGUAGE_CODE)),
                                  "status": Status_code.no_content})
        return self.destroy(request,lang_code=request.LANGUAGE_CODE, *args, **kwargs)