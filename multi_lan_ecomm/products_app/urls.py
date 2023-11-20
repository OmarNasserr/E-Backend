from django.urls import path

from .views.PUT_DEL_requests import ProductDetailUpdateDelete      
from .views.POST_requests import ProductCreate
from .views.GET_requests import ProductList

from .product_variations_views.PUT_DEL_requests import ProductVariationDetailUpdateDelete      
from .product_variations_views.POST_requests import ProductVariationCreate
from .product_variations_views.GET_requests import ProductVariationList

from .product_color_views.GET_requests import ProductColorList
from .product_color_views.POST_requests import ProductColorCreate
from .product_color_views.PUT_DEL_requests import ProductColorDetailUpdateDelete

urlpatterns = [
     
     path('product_variations/create/', ProductVariationCreate.as_view(),
         name='product-variation-create'),
    path('product_id/<path:product_id>/product_variations/list/', ProductVariationList.as_view(),
         name='product-varaitions-list-by-product_id'),
    path('product_variations/<path:product_varaition_id>/details/',
         ProductVariationDetailUpdateDelete.as_view(), name='product-variation-details'),
    
     
     path('product_color/create/', ProductColorCreate.as_view(),
         name='product-color-create'),
    path('product_id/<path:product_id>/product_color/list/', ProductColorList.as_view(),
         name='product-color-list-by-product_id'),
    path('product_color/<path:product_color_id>/details/',
         ProductColorDetailUpdateDelete.as_view(), name='product-color-details'),
     
     
    path('create/', ProductCreate.as_view(),
         name='product-create'),
    path('subsubcategory_id/<path:subsubcategory_id>/list/', ProductList.as_view(),
         name='product-list-by-subsubcategory_id'),
    path('<path:product_id>/details/',
         ProductDetailUpdateDelete.as_view(), name='product-detail'),

]
