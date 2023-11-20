import ast
import json
from rest_framework.exceptions import ValidationError
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
from rest_framework.fields import SkipField
from django.conf import settings

from helper_files.images_helper import Images_Helper

from .cryptography import AESCipher
from .multi_languages import Multi_Languages_Support


aes = AESCipher(settings.SECRET_KEY[:16], 32)


class SerializerHelper():

    # is_valid is overrided to return bool and a error value if exist, this is done to keep a
    # consistent response shape {'message':'xxx',...}, therefore the error message is extracted
    # and returned to the response to be represented in a proper format.
    def is_valid(self, *, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        if len(self.errors.keys()) != 0:
            print(self._errors)
            err = list(self.errors.keys())[0]
            if self.errors[str(err)][0] == "This field is required.":
                errReturned = "The field '"+str(err)+"' is required"
            else:
                errReturned = self.errors[str(err)][0]
        else:
            errReturned = "no errors were returned"

        return not bool(self._errors), errReturned

    def is_valid_multi_languages(self, *, raise_exception=False, languages, used_language):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        if len(self.errors.keys()) != 0:
            print("err START", self._errors)
            error_key = list(self.errors.keys())[0]
            if error_key == 'languages':
                try:
                    lan_code = list(list(self.errors[str(error_key)]))[0]
                    field_name = list(
                        list(self.errors[str(error_key)][str(lan_code)]))[0]
                    err = list(
                        list(self.errors[str(error_key)][str(lan_code)][str(field_name)]))[0]
                except:
                    err = 'languages '+str(self.errors[str(error_key)][0])
                    
            elif error_key == 'uploaded_images':
                try:
                    err = list(list(self.errors[str(error_key)]))[0]
                    if used_language in languages:
                        if 'Upload a valid image' in err:
                            err = Multi_Languages_Support.return_err_message(used_language=used_language,
                                                            msgEN="unsupported image format, supported formats "+str(Images_Helper.supported_formats), 
                                                            msgAR='تنسيق الصورة غير مدعوم ، التنسيقات المدعومة '+str(Images_Helper.supported_formats))
                        else:
                            err = Multi_Languages_Support.return_err_message(used_language=used_language,
                                                            msgEN='must upload a photo', msgAR='يجب رفع صورة')
                except:
                    err = 'must upload a photo'
            
            else:
                if 'pk' or 'معرف العنصر' in list(self._errors[str(list(self.errors.keys())[0])])[0] :
                    err = Multi_Languages_Support.return_err_message(used_language=used_language,
                                                msgEN='Invalid item ID - The item does not exist.',
                                                msgAR="معرف العنصر غير صالح - العنصر غير موجود.",
                                                )
                else:
                    err=list(self._errors[str(list(self.errors.keys())[0])])[0]

            errReturned = err
        else:
            errReturned = "no errors were returned"

        return not bool(self._errors), errReturned

    # to_representation function is used to represent data in response, and as we might have
    # returned encrypted data or data that we would like to be represented as encrypted data
    # like object_id
    # therefore the fields_to_be_decrypted is a list of fields that are stored in db encrypted
    # and we would like to decrypt and represent them
    # fields_to_be_encrypted is list of fields that aren't encrypted in the database but they
    # are sensitive, therefore we need to encrypt them in the response

    def to_representation(
        self, instance,
        fields_to_be_decrypted,
        fields_to_be_encrypted,
        fields_to_be_added={}
    ):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            check_for_none = attribute.pk if isinstance(
                attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                # put the attributes that are encrypted in the db and
                # you want them to be decrypted
                if field.field_name in fields_to_be_decrypted:
                    ret[field.field_name] = aes.decrypt(
                        field.to_representation(attribute))
                # put the attributes that are not encrypted in the db and
                # you want them to be showed encrypted (Foriegn Keys, ids, etc)
                elif field.field_name in fields_to_be_encrypted:
                    ret[field.field_name] = aes.encrypt(
                        str(field.to_representation(attribute)))
                else:
                    ret[field.field_name] = field.to_representation(attribute)
        if fields_to_be_added is not {}:
            for key in fields_to_be_added.keys():
                ret[str(key)] = fields_to_be_added[str(key)]

        return ret
    
    # def update_multi_languages():
    
    
    