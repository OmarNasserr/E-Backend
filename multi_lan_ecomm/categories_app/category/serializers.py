from dataclasses import field
from rest_framework import serializers
from django.conf import settings
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import Category,CategoryImage
from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher
from .category_helper import Category_Helper


aes = AESCipher(settings.SECRET_KEY[:16], 32)

class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoryImage
        fields=["id","image"]
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
        
class CategorySerializer(TranslatableModelSerializer):
    
    languages = TranslatedFieldsField(shared_model=Category)
    
    # subcategories=serializers.StringRelatedField(many=True,read_only=True)
    category_image=CategoryImageSerializer(many=True,read_only=True)
    
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=1000000,use_url=False),
        write_only=True,
    )

    class Meta:
        model=Category
        fields='__all__'
    
    
    def create(self, validated_data):
        
        request=self.context.get('request')
        uploaded_images=validated_data.pop('uploaded_images')
        
        category=Category_Helper.category_create(request=request.data)
        CategoryImage.objects.create(category=category, image=uploaded_images[0])
        
        return category
    
    def update(self, instance, validated_data):
        
        if 'uploaded_images' in validated_data.keys():
            uploaded_images=validated_data.pop('uploaded_images')
            
            #if category was created with no img or its img was deleted and we wanted to update the category
            #img then we have to check the existance of the img first if not then we create one
            try:
                category_image=CategoryImage.objects.filter(category=instance)[0]
            except:
                category_image=CategoryImage.objects.create(category=instance)
            category_image.image=uploaded_images[0]
            category_image.save()
        
        return super().update(instance, validated_data)
        
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id',]
        )
    
    def is_valid(self, *, raise_exception=False,languages,used_language):
        return SerializerHelper.is_valid_multi_languages(
            self=self,raise_exception=raise_exception,languages=languages,used_language=used_language
            )