import json
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from helper_files.images_helper import Images_Helper
from helper_files.multi_languages import Multi_Languages_Support

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class SubsubcategoryValidations():
    
    def check_sub_sub_category_create(data, valid, err, used_language, languages):  # type: ignore
        if valid:
            languages_data = data['languages']
            for i in range(len(languages)):
                if len(languages_data['en']['subsubcategory_name']) != 0:
                    if len(languages_data[languages[i]]['subsubcategory_name']) != 0:
                        if len(languages_data[languages[i]]['subsubcategory_name']) < 3:
                            message = Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Sub-sub-category's name can't be less than three characters.",
                                msgAR="يجب الا يقل اسم الفئة الفرعية عن ثلاث احرف"
                            )
                            return Response(data={'message': message,
                                                  "status": Status_code.bad_request},
                                            status=Status_code.bad_request)
                else:
                    return Response(data={'message': "English sub-sub-category's name can't be empty",
                                          "status": Status_code.bad_request},
                                    status=Status_code.bad_request)

            else:
                message = Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Sub-sub-category was created successfully.",
                                msgAR="تم إنشاء فئة فرعية فرعية بنجاح."
                            )
                return Response(data={"message": message    , "status": Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)
    
    def check_sub_sub_category_update(data, valid, err, used_language, languages,):  # type: ignore
        if valid:
            message = Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Item was updated successfully.",
                                msgAR="تم تحديث العنصر بنجاح."
                            )
            return Response(data={"message": message, "status": Status_code.created},
                            status=Status_code.updated)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)
