from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from helper_files.permissions import permission_denied

from .serializers import ColorSerializer
from .models import Color
from .pagination import ColorAppPagination
from helper_files.status_code import Status_code
from .validations import ColorAppValidations

from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class ColorsList(generics.ListAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    
    pagination_class=ColorAppPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields=['color_name','hex_color']
    search_fields = ['color_name','hex_color']
    
    def get(self, request, *args, **kwargs):
        ColorAppPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
    


class ColorCreate(generics.CreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    # permission_classes=[AdminOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid,err=serializer.is_valid(raise_exception=False)
        response = ColorAppValidations.validate_color_create(self,self.request.data,valid,err,str(request.LANGUAGE_CODE))
        if response.status_code == Status_code.created:
            serializer.save()

        return response


class ColorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ColorSerializer
    # permission_classes=[AdminOrPlaygroundOwner]
    
    # def permission_denied(self, request):
    #     Permissions.permission_denied(self=self ,request=request)
    
    # def check_permissions(self, request):
    #     try:
    #         color_id = aes.decrypt(str(self.kwargs['color_id']))
    #         color=Color.objects.filter(pk=int(color_id))
    #         obj = color[0]
    #     except:
    #         return Response(data={"message": "Color wasn't found.",
    #                           "status":Status_code.no_content},status=Status_code.no_content) 
        # return permission_denied.check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            color_id = aes.decrypt(str(self.kwargs['color_id']))
            color=Color.objects.filter(pk=int(color_id))
            obj = color[0]
        except:
            return ValueError('wrong id format')
        if color.count() == 0:
            return ValueError('wrong id format')
        self.check_object_permissions(self.request, obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'colors_app.models.Color'>":
            return Response(data={"message": "Color wasn't found.",
                              "status":Status_code.no_content},)
        else:    
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            valid,err=serializer.is_valid(raise_exception=True)
            response=ColorAppValidations.validate_color_update(self,self.request.data,valid,err,str(request.LANGUAGE_CODE))
            if response.status_code == Status_code.updated:
                serializer.save()
                response.data['color']=serializer.data

            return response
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(str(type(instance)))
        if str(type(instance)) != "<class 'colors_app.models.Color'>":
            return Response(data={"message": "Color wasn't found.",
                              "status":Status_code.no_content})
        serializer = self.get_serializer(instance)
        return Response(data={"message":"color was retrieved successfully",
                              "status": Status_code.success,'color':serializer.data,},
                        status=Status_code.success)
  
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'colors_app.models.Color'>":
            return Response(data={"message": "Color wasn't found.",
                              "status":Status_code.no_content},)
        return self.destroy(request,lang_code=request.LANGUAGE_CODE, *args, **kwargs)