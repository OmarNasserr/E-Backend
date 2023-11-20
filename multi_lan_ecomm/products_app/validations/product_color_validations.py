from rest_framework.response import Response
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from helper_files.images_helper import Images_Helper
from helper_files.multi_languages import Multi_Languages_Support    



aes = AESCipher(settings.SECRET_KEY[:16], 32)


class ProductColorValidations():

    def check_product_color_create(data, valid, err, used_language,):  # type: ignore
        if valid:
                message = Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Product color was created successfully.",
                                msgAR="تم إنشاء لون المنتج بنجاح."
                            )
                return Response(data={"message": message, "status": Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)
    
    
    def check_product_color_update(data, valid, err, used_language,):  # type: ignore
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