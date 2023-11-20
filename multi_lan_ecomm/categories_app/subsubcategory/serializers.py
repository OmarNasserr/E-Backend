from dataclasses import field
from rest_framework import serializers
from rest_framework.exceptions import  ValidationError
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject 
from rest_framework.fields import SkipField
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import SubSubCategory,SubSubCategoryImage
from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher
from .subsubcategory_helper import Subsubcategories_Helper
from products_app.serializers import ProductSerializer


aes = AESCipher(settings.SECRET_KEY[:16], 32)

class SubSubCategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubSubCategoryImage
        fields=["id","image",]
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
        
class SubSubCategorySerializer(TranslatableModelSerializer):
    
    languages = TranslatedFieldsField(shared_model=SubSubCategory)
    
    # category_name=serializers.SerializerMethodField('get_category_name')
    # subcategory_name=serializers.SerializerMethodField('get_sub_category_name')
    
    subsubcategory_image=SubSubCategoryImageSerializer(many=True,read_only=True)
    
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=1000000,use_url=False),
        write_only=True,
    )
    
    products=ProductSerializer(many=True,read_only=True)
    
    #if we want only product name to appear
    # products=serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model=SubSubCategory
        fields='__all__'
        
        
    def create(self, validated_data):
        
        request=self.context.get('request')
        uploaded_images=validated_data.pop('uploaded_images')
        
        subsubcategory=Subsubcategories_Helper.subsubcategory_create(request=request.data)
        SubSubCategoryImage.objects.create(subsubcategory=subsubcategory, image=uploaded_images[0])
        
        return subsubcategory
    
    def update(self, instance, validated_data):
        
        if 'uploaded_images' in validated_data.keys():
            uploaded_images=validated_data.pop('uploaded_images')
            try:
                subsubcategory_image=SubSubCategoryImage.objects.filter(subsubcategory=instance)[0]
            except:
                subsubcategory_image=SubSubCategoryImage.objects.create(subsubcategory=instance)
            subsubcategory_image.image=uploaded_images[0]
            subsubcategory_image.save()
        
        return super().update(instance, validated_data)
    
    # def get_category_name(self,subsubcategory):
    #     category=subsubcategory.subcategory_id.category_id.category_name
    #     return category
    
    # def get_sub_category_name(self,subsubcategory):
    #     subcategory=subsubcategory.subcategory_id.subcategory_name
    #     return subcategory
    
     
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id','subcategory']
        )
    
    def is_valid(self, *, raise_exception=False,languages,used_language):
        return SerializerHelper.is_valid_multi_languages(
            self=self,raise_exception=raise_exception,languages=languages,used_language=used_language)