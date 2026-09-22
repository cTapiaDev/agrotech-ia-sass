from django.urls import path
from . import views

urlpatterns = [
    path('fields/', views.FarmFieldListView.as_view(), name='farmfield_list'),
    path('fields/new/', views.FarmFieldCreateView.as_view(), name='farmfield_create'),
    path('fields/<int:pk>/edit/', views.FarmFieldUpdateView.as_view(), name='farmfield_update'),
    path('fields/<int:pk>/delete/', views.FarmFieldDeleteView.as_view(), name='farmfield_delete'),
    path('crops/', views.CropListView.as_view(), name='crop_list'),
    path('crops/new/', views.CropCreateView.as_view(), name='crop_create'),
    path('crops/<int:pk>/edit/', views.CropUpdateView.as_view(), name='crop_update'),
    path('crops/<int:pk>/delete/', views.CropDeleteView.as_view(), name='crop_delete'),
]