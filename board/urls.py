from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('com2_list', views.com2_list, name='com2_list'),
    path('com2_upload/', views.com2_upload, name='com2_upload'),
    path('com2_detail/<int:pk>/', views.com2_detail, name='com2_detail'),
    path('com1_list', views.com1_list, name='com1_list'),
    path('com1_detail/<int:pk>/', views.com1_detail, name='com1_detail'),
    path('com1_upload/', views.com1_upload, name='com1_upload'),
    path('py_list', views.py_list, name='py_list'),

]
