from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import re

from helper_files.multi_languages import Multi_Languages_Support
from helper_files.status_code import Status_code


class UserAppValidation():
    def validate_user_create(data,valid,err,used_language):
        
        email_regex="(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|'(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*')@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        
        if valid:
            if data['password_confirm'] != data['password']:
                return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="password confirm does not match password.",
                                msgAR="تأكيد كلمة المرور لا يتطابق مع كلمة المرور."
                            ),
                                'status':Status_code.bad_request},
                                status=Status_code.bad_request)

            if User.objects.filter(email=data['email']).exists():
                return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="this email already exists.",
                                msgAR="هذا البريد الإلكتروني موجود بالفعل."
                            ),
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            
            if User.objects.filter(username=data['username']).exists():
                return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="this user already exists.",
                                msgAR="هذا المستخدم موجود بالفعل."
                            ),
                                'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            
            if not re.match(email_regex,data['email']):
                return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="invalid email address.",
                                msgAR="عنوان البريد الإلكتروني غير صالح."
                            ),
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            
            if len(data['first_name'])<2:
                return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="first name must be at least 2 characters.",
                                msgAR="يجب أن يتكون الاسم الأول من حرفين على الأقل."
                            ),
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            
            if len(data['last_name'])<2:
                return Response(data={'message':Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="last name must be at least 2 characters.",
                                msgAR="يجب أن يتكون اسم العائلة من حرفين على الأقل."
                            ),
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
           
            else:
               return Response(status=Status_code.success)
        else:
            return Response(data={'message':str(err),"status":Status_code.bad_request},
                                    status=Status_code.bad_request)