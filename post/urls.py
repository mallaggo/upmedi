from django.contrib import admin
from django.urls import path, include
from . import views
app_name='post'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/comment/', views.comment_create, name='comment_create'),

    ]