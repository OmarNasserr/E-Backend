from rest_framework.response import Response
from rest_framework import status
import re

from helper_files.multi_languages import Multi_Languages_Support

from .models import Color
from helper_files.status_code import Status_code


class ColorAppValidations():

    def validate_color_create(self, data, valid, err,used_language):
        hex_regex = "^#(?:[0-9a-fA-F]{3}){1,2}$"

        if valid:
            if not re.match(hex_regex, data['hex_color']):
                return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Color's hex_color doesn't match time hex code format.",
                                msgAR="لا يتطابق hex_color للون مع تنسيق الكود السداسي العشري للوقت."
                            ),
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if len(data['color_name'])<3:
                return Response(data={'message':Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Color's color_name can not be less than 3 characters.",
                                msgAR="لا يمكن أن يكون اسم Color_name أقل من ثلاث أحرف."
                            ),
                                'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            else:
                
                 return Response(data={"message": Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Color was created successfully.",
                                msgAR="تم إنشاء اللون بنجاح."
                            ),
                                    'status': Status_code.created},
                                    status=Status_code.created)
               
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)


    def validate_color_update(self, data, valid, err,used_language):
        hex_regex = "^#(?:[0-9a-fA-F]{3}){1,2}$"

        if valid:
            if 'hex_color' in data.keys():
                if not re.match(hex_regex, data['hex_color']):
                    return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Color's hex_color doesn't match time hex code format.",
                                msgAR="لا يتطابق hex_color للون مع تنسيق الكود السداسي العشري للوقت."
                            ),
                                        'status': Status_code.bad_request},
                                    status=Status_code.bad_request)
                else:
                    return Response(data={"message": Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Color was updated successfully.",
                                msgAR="تم تحديث اللون بنجاح."
                            ),
                                          'status': Status_code.updated},
                                    status=Status_code.updated)
            if 'color_name' in data.keys():
                if len(data['color_name'])<3:
                    return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Color's color_name can not be less than 3 characters.",
                                msgAR="لا يمكن أن يكون اسم Color_name أقل من ثلاث أحرف."
                            ),
                                        'status': Status_code.bad_request},
                                    status=Status_code.bad_request)
                else:
                    return Response(data={"message": Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Color was updated successfully.",
                                msgAR="تم تحديث اللون بنجاح."
                            ),
                                          'status': Status_code.updated},
                                    status=Status_code.updated)
            else:
                return Response(data={"message": Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="No data was given to update Color.",
                                msgAR="لا توجد بيانات لتحديث اللون."
                            ),
                                'status': Status_code.bad_request},
                                status=Status_code.bad_request)
               
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)