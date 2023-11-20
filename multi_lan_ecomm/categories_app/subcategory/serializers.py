from dataclasses import field
from rest_framework import serializers
from rest_framework.exceptions import  ValidationError
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject 
from rest_framework.fields import SkipField
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import SubCategory,SubCategoryImage
from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher
from .subcategory_helper import Subcategory_Helper


aes = AESCipher(settings.SECRET_KEY[:16], 32)


class SubCategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategoryImage
        fields=["id","image",]
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
        
        
class SubCategorySerializer(TranslatableModelSerializer):
    
    languages = TranslatedFieldsField(shared_model=SubCategory)
    
    # category_name=serializers.SerializerMethodField('get_category_name')
    subcategory_image=SubCategoryImageSerializer(many=True,read_only=True)
    
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=1000000,use_url=False),
        write_only=True,
    )

    class Meta:
        model=SubCategory
        fields='__all__'
        
        
    def create(self, validated_data):
        
        request=self.context.get('request')
        uploaded_images=validated_data.pop('uploaded_images')
        
        subcategory=Subcategory_Helper.subcategory_create(request=request.data)
        SubCategoryImage.objects.create(subcategory=subcategory, image=uploaded_images[0])
        
        return subcategory
    
    
    def update(self, instance, validated_data):
        
        if 'uploaded_images' in validated_data.keys():
            uploaded_images=validated_data.pop('uploaded_images')
            try:
                subcategory_image=SubCategoryImage.objects.filter(subcategory=instance)[0]
            except:
                subcategory_image=SubCategoryImage.objects.create(subcategory=instance)
                
            subcategory_image.image=uploaded_images[0]
            subcategory_image.save()
        
        return super().update(instance, validated_data)
    
    # def get_category_name(self,subcategory):
    #     category=subcategory.category_id.category_name
    #     return category
    
     
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id','category']
        )
    
    def is_valid(self, *, raise_exception=False,languages,used_language):
        return SerializerHelper.is_valid_multi_languages(
            self=self,raise_exception=raise_exception,languages=languages,used_language=used_language)
