from urllib import request
from django.urls import path,include
from .views import SizeCreate,SizeDetail,SizesList

urlpatterns = [
    path('create/',SizeCreate.as_view(),name='size-create'),
    path('list/',SizesList.as_view(),name='size-list'),
    path('<path:size_id>/detail/',SizeDetail.as_view(),name='size-detail'),
]
