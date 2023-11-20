from django.urls import path

from .subsubcategory.views.POST_requests import SubSubCategoryCreate

from .category.views.PUT_DEL_requests import CategoryDetailUpdateDelete

from .category.views.GET_requests import CategoryList
from .category.views.POST_requests import CategoryCreate
from .subcategory.views.POST_requests import SubCategoryCreate
from .subcategory.views.PUT_DEL_requests import SubCategoryDetailUpdateDelete
from .subcategory.views.GET_requests import SubCategoryList
from .subsubcategory.views.GET_requests import SubSubCategoryList
from .subsubcategory.views.PUT_DEL_requests import SubSubCategoryDetailUpdateDelete

urlpatterns = [
    path('subsubcategory/create/',
         SubSubCategoryCreate.as_view(), name='subsubcategory-create'),
    path('subcategory/<path:subcategory_id>/subsubcategory/list/', SubSubCategoryList.as_view(),
         name='subsubcategories-list-by-subcategory-name'),
    path('subsubcategory/<path:subsubcategory_id>/details/',
         SubSubCategoryDetailUpdateDelete.as_view(), name='subsubsubcategory-detail'),

    path('subcategory/create/', SubCategoryCreate.as_view(),
         name='subcategory-create'),
    path('category/<path:category_id>/subcategory/list/', SubCategoryList.as_view(),
         name='subcategories-list-by-category-name'),
    path('subcategory/<path:subcategory_id>/details/',
         SubCategoryDetailUpdateDelete.as_view(), name='subcategory-detail'),


    path('category/create/', CategoryCreate.as_view(), name='category-create'),
    path('category/list/', CategoryList.as_view(), name='category-list'),
    path('category/<path:category_id>/details/', CategoryDetailUpdateDelete.as_view(),
         name='category-update-delete'),
]
