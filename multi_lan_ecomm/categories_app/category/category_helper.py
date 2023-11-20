from categories_app.category.models import Category
from categories_app.category.validations import CategoryValidations
from helper_files.multi_languages import Multi_Languages_Support
from helper_files.status_code import Status_code


class Category_Helper():
    
    
    def category_create(request):
        languages=request['languages']
        available_languages=Multi_Languages_Support.get_availabe_languages()
        
        category=Category.objects.create()
        
        for i in range(len(available_languages)):
            category.set_current_language(str(available_languages[i])) 
            category.category_name=languages[str(available_languages[i])]['category_name']
            category.description=languages[str(available_languages[i])]['description']
            category.save() 
        
        return category
    
    
    def category_update(self, request,instance ,*args, **kwargs):
        languages = Multi_Languages_Support.get_availabe_languages()
        lang_code = str(request.LANGUAGE_CODE)
        
        try:
            request.data._mutable = True
        except:
            pass
        keys=list(request.data.keys())
        if 'languages' in keys:
            request.data['languages']=Multi_Languages_Support.convert_request_to_json(
                request=request,lang_code=lang_code
                )
            
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        valid,err=serializer.is_valid(
            raise_exception=False, languages=languages, used_language=lang_code)
        
        response = CategoryValidations.check_category_update(
            request.data, valid, err, used_language=lang_code,languages=languages)
        
        if response.status_code==Status_code.updated:
            self.perform_update(serializer)
            response.data['item']=serializer.data

        #This is done because the prefetched data could become obsolete after the update. 
        # So you can override the update method and redo the prefetch after the update
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        
        return response