from operator import truediv
from rest_framework import permissions
from helper_files.custom_exceptions import PermissionDenied,NotAuthenticated



################################################################
# in this file we are creating our own permissions for accessing data
# this function is from rest_framework documentaion 'Custom Permissions'
################################################################

class IsAdminOrReadOnly(permissions.IsAdminUser):
    
    
    #this allows the admin user only to edit it, but normal user can only read
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True                                            
        else:
            return bool(request.user and request.user.is_superuser)
    

class IsProfileUserOrAdminOrReadOnly(permissions.BasePermission):
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:#safe_method is GET
            return True                               #and unsafe_method are PUT,POST,DELETE                  
        else:
            return str(obj)==str(request.user) or request.user.is_superuser


################################
#overrided the permission_denied method to control the error message
################################
def permission_denied(self, request):
    if request.authenticators and not request.successful_authenticator:
        raise NotAuthenticated()
    raise PermissionDenied()

################################
#overrided the check_object_permissions method because the method has arguments that 
#we don't want like 'message' and 'code'
################################
def check_object_permissions(self, request, obj):
    for permission in self.get_permissions():
        if not permission.has_object_permission(request, self, obj):
            self.permission_denied(
                request,
            )