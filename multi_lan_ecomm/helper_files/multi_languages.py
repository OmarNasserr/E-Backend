from django.conf import settings
from rest_framework.response import Response
from rest_framework import exceptions, status
import json



class Multi_Languages_Support:

    def get_availabe_languages():
        available_languages = []
        languages = list(settings.LANGUAGES)
        for i in range(len(languages)):

            available_languages.append(list(languages[i])[0])

        return available_languages
    
    def return_err_message(used_language,msgEN,msgAR):
        languages = Multi_Languages_Support.get_availabe_languages()
        if used_language in languages:
            if used_language=='en':
                return msgEN
            elif used_language == 'ar':
                return msgAR
        else:
            return "unspported language was given"
        
        
    def convert_request_to_json(request,lang_code):
        
        #this will catch error if languages field wasn't given 
        try:
            request.data['languages'] = json.loads(str(request.data['languages']))
            
            return request.data['languages']
        except:
            message = Multi_Languages_Support.return_err_message(
                                used_language=lang_code, 
                                msgEN="languages field is required",
                                msgAR="حقل اللغات مطلوب"
                            )
            return Response(data={'message': message,
                                          "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
    
    def not_found_message(lang_code):
        
        return Multi_Languages_Support.return_err_message(
                                used_language=lang_code, 
                                msgEN="Item was not found.",
                                msgAR=".لم يتم العثور على العنصر"
                            )
    
        