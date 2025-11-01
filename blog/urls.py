from django.urls import path
from . import views
app_name='blog'


urlpatterns = [
    path('',views.index,name='index'),
    # path('video/<int:pk>/', views.video_detail, name='video_detail'),


    ]