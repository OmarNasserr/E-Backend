from rest_framework import serializers
from django.conf import settings
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from colors_app.models import Color
from colors_app.serializers import ColorSerializer
from sizes_app.models import Size

from sizes_app.serializers import SizeSerializer

from .models import Product,ProductImage,ProductColor,ProductVariations,ProductThumbnailImage
from .product_helper import Product_Helper
from helper_files.serializer_helper import SerializerHelper

#########################################################
#
# NESTED SERIALIZATION
# ProductSerializer
#   ProductThumbnailImageSerializer
#   ProductVariationsSerializer
#      SizeSerializer
#      ProductColorSerializer
#           ColorSerialzier
#           ProductImageSerialzier
#
# ProductSerialzier shows the thumbnail image details using the ProductThumbnailImageSerializer,
# and the stock using ProductVariationsSerializer
#
# ProductVariationsSerializer shows size details using SizeSerializer,
# and the ProductColor combination using ProductColorSerializer
# 
# ProductColorSerializer shows the color details using ColorSerialzier,
# and the prodcut color images details using ProductImageSerialzier
#
#########################################################

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=["id","image",]
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )

class ProductThumbnailImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductThumbnailImage
        fields=["id","image",]
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
        
class ProductColorSerializer(serializers.ModelSerializer):
    
    color=ColorSerializer(read_only=True)
    product_color_images=ProductImageSerializer(many=True,read_only=True)
    
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=1000000,use_url=False),
        write_only=True,
    )
        
    
    def create(self, validated_data):
        
        request=self.context.get('request')
        uploaded_images=validated_data.pop('uploaded_images')
                
        product=request.data['product']
        color=request.data['color']
        
        color=Color.objects.filter(pk=request.data['color'])[0]
        product=Product.objects.filter(pk=request.data['product'])[0]
        
        productColor=ProductColor.objects.create(product=product,color=color)
        
        for image in uploaded_images:
            ProductImage.objects.create(productColor=productColor,image=image)
        
        
        return productColor
    
    def update(self, instance, validated_data):
        
        if 'uploaded_images' in validated_data.keys():
            uploaded_images=validated_data.pop('uploaded_images')
            
                
            for image in uploaded_images:
                ProductImage.objects.create(productColor=instance,image=image)
                
        
        return super().update(instance, validated_data)
    
    class Meta:
        model=ProductColor
        fields=['id','uploaded_images','color','product_color_images']
    
    def is_valid(self, *, raise_exception=False,languages,used_language):
        return SerializerHelper.is_valid_multi_languages(
            self=self,raise_exception=raise_exception,languages=languages,used_language=used_language
            )
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id','product']
        )
        
class ProductVariationsSerializer(serializers.ModelSerializer):
    
    size=SizeSerializer(many=True,read_only=True)
    product_color_variations=ProductColorSerializer(many=True,read_only=True)
    
    def create(self, validated_data):
        
        request=self.context.get('request')
        
        product=request.data['product']
        size=request.data['size']
        product_color_variations=request.data['product_color_variations']
        number_in_stock=request.data['number_in_stock']
        
        product_obj=Product.objects.get(pk=product)
        size_obj=Size.objects.get(pk=size)
        product_color_variations_obj=ProductColor.objects.get(id=product_color_variations)
        
        productVariation=ProductVariations.objects.create(product=product_obj,
                                                            number_in_stock=number_in_stock)
        productVariation.size.add(size_obj)
        productVariation.product_color_variations.add(product_color_variations_obj)
        
        
        return productVariation
    
    class Meta:
        model=ProductVariations
        fields=('id','product','product_color_variations','size','number_in_stock')
        
    
    def is_valid(self, *, raise_exception=False,languages,used_language):
        return SerializerHelper.is_valid_multi_languages(
            self=self,raise_exception=raise_exception,languages=languages,used_language=used_language
            )
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id','product']
        )

class ProductSerializer(TranslatableModelSerializer):
    
    languages = TranslatedFieldsField(shared_model=Product)
    thumbnail=ProductThumbnailImageSerializer(many=True,read_only=True)
    stock=ProductVariationsSerializer(many=True,read_only=True)
    
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=1000000,use_url=False),
        write_only=True,
    )        

    class Meta:
        model=Product
        fields='__all__'
        read_only_fields=('total_num_in_stock',)
        
        
    def create(self, validated_data):
        
        request=self.context.get('request')        
        
        uploaded_images=validated_data.pop('uploaded_images')
        product=Product_Helper.product_create(request=request.data)
        
        try:
            #since we only need one image as a thumbnail therefore we will just take the first image
            ProductThumbnailImage.objects.create(product=product,image=uploaded_images[0])
        except:
            #this is just a precautionary exception as uploaded images is a mandatory field
            print("no images was uploaded")
            pass
                
        return product

    def update(self, instance, validated_data):
        
        if 'uploaded_images' in validated_data.keys():
            uploaded_images=validated_data.pop('uploaded_images')
            
            #if a product was created with no img or its img was deleted and we wanted to update the product
            #thumbnail img then we have to check the existance of the img first if not then we create one
            try:
                thumbnail=ProductThumbnailImage.objects.filter(product=instance)[0]
            except:
                thumbnail=ProductThumbnailImage.objects.create(product=instance)
            thumbnail.image=uploaded_images[0]
            thumbnail.save()
        
        return super().update(instance, validated_data)
        
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id','subsubcategory']
        )
    
    def is_valid(self, *, raise_exception=False,languages,used_language):
        return SerializerHelper.is_valid_multi_languages(
            self=self,raise_exception=raise_exception,languages=languages,used_language=used_language
            )