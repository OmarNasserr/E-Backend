from rest_framework.response import Response
from rest_framework import status
import re
from helper_files.multi_languages import Multi_Languages_Support

from helper_files.status_code import Status_code


class SizeAppValidations():
    av_sizes = ['XS','S','M','L','XL','XXL','XXXL','XXXXL','XXXXXL','37','38','39','40',
                    '41','42','43','44','45','46',]
    
    def validate_size_create(self, data, valid, err,used_language):

        if valid:
            if data['size_name'] not in SizeAppValidations.av_sizes:
                return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Size can only be on of "+str(SizeAppValidations.av_sizes),
                                msgAR=" يمكن أن يكون المقاس فقط واحد من"+str(SizeAppValidations.av_sizes),
                            ),
                                'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            else:
                
                 return Response(data={"message": Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Size was created successfully.",
                                msgAR="تم إنشاء المقاس بنجاح.",
                            ),
                                'status': Status_code.created},
                                status=Status_code.created)
               
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)


    def validate_size_update(self, data, valid, err,used_language):
        
        if valid:
            if 'size_name' in data.keys():
                if data['size_name'] not in SizeAppValidations.av_sizes:
                    return Response(data={'message':Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Size can only be on of "+str(SizeAppValidations.av_sizes),
                                msgAR=" يمكن أن يكون المقاس فقط واحد من"+str(SizeAppValidations.av_sizes),
                            ),
                                        'status': Status_code.bad_request},
                                    status=Status_code.bad_request)
                else:
                    
                    return Response(data={"message": Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="Size was created successfully.",
                                msgAR="تم إنشاء المقاس بنجاح.",
                            ),
                                            'status': Status_code.created},
                                        status=Status_code.created)
            else:
                return Response(data={'message': Multi_Languages_Support.return_err_message(
                                used_language=used_language,
                                msgEN="size_name can't be empty.",
                                msgAR="لا يمكن أن يكون size_name فارغًا.",
                            ),
                                "status": Status_code.bad_request},
                                status=Status_code.bad_request)
                
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)