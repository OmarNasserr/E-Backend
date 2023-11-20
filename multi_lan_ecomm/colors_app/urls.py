from urllib import request
from django.urls import path,include
from .views import ColorsList,ColorCreate,ColorDetail

urlpatterns = [
    path('create/',ColorCreate.as_view(),name='color-create'),
    path('list/',ColorsList.as_view(),name='color-list'),
    path('<path:color_id>/detail/',ColorDetail.as_view(),name='color-detail'),
]
