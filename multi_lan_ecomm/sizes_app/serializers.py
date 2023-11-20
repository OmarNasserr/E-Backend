from rest_framework import serializers
from django.conf import settings


from .models import Size
from helper_files.serializer_helper import SerializerHelper

class SizeSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model=Size
        fields=["id","size_name"]
        
    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self,raise_exception=raise_exception)
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )