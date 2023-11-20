from categories_app.subcategory.models import SubCategory
from categories_app.subsubcategory.validations import SubsubcategoryValidations
from helper_files.status_code import Status_code
from .models import SubSubCategory
from helper_files.multi_languages import Multi_Languages_Support



class Subsubcategories_Helper():
    
    def subsubcategory_create(request):
        languages=request['languages']
        available_languages=Multi_Languages_Support.get_availabe_languages()
        
        subcategory=SubCategory.objects.get(pk=request['subcategory'])
        subsubcategory=SubSubCategory.objects.create(subcategory=subcategory)
        
        
        for i in range(len(available_languages)):
            subsubcategory.set_current_language(str(available_languages[i])) 
            subsubcategory.subsubcategory_name=languages[str(available_languages[i])]['subsubcategory_name']
            subsubcategory.description=languages[str(available_languages[i])]['description']
            subsubcategory.save() 
        
        return subsubcategory
    
    def subsubcategory_update(self, request,instance ,*args, **kwargs):
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
        
        response = SubsubcategoryValidations.check_sub_sub_category_update(
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