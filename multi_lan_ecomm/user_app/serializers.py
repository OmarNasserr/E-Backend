from dataclasses import fields
from email.policy import default
from django.contrib.auth.models import User
from rest_framework import serializers
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject 
from rest_framework.fields import SkipField
from django.conf import settings
from rest_framework import status

from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher


aes = AESCipher(settings.SECRET_KEY[:16], 32)


class RegisterationSerializer(serializers.ModelSerializer):
    password_confirm=serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model=User
        fields=['username','email','password','password_confirm','is_staff','first_name','last_name',
                'is_superuser','id']
        extra_kwargs={
            'password':{'write_only':True},
            'email':{'required':True},
            'is_staff':{'default':False},
            'is_superuser':{'default':False},
        }
    
    
    def save(self,validated_data):
        
        account=User(email=validated_data['email'],username=validated_data['username'],
                     is_staff=validated_data['is_staff'],first_name=validated_data['first_name'],
                     last_name=validated_data['last_name'],
                     is_superuser=validated_data['is_superuser'],)
        account.set_password(validated_data['password'])
        account.save()
        
        return account

    
    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self,raise_exception=raise_exception)
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
    

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['username','email','is_staff','first_name','last_name',
                'is_superuser','id']
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )