from rest_framework.response import Response
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from helper_files.images_helper import Images_Helper
from helper_files.multi_languages import Multi_Languages_Support    



aes = AESCipher(settings.SECRET_KEY[:16], 32)


class ProductVariationValidations():

    def check_product_variation_create(data, valid, err, used_language,):  # type: ignore
        if valid:
            if int(str(data['number_in_stock']))<1:
                message = Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Number in stock can not be less than 1.",
                                msgAR="لا يمكن أن يكون الرقم المتوفر أقل من 1."
                            )
            else:
                message = Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Product variation was created successfully.",
                                msgAR="تم إنشاء صيغة المنتج بنجاح."
                            )
            
            return Response(data={"message": message, "status": Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)
    
    
    def check_product_variation_update(data, valid, err, used_language,):  # type: ignore
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