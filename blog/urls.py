from django.urls import path,include
from . import views
app_name='blog'


urlpatterns = [
    path('',views.index,name='index'),
    path('video_detail/<int:pk>/',views.video_detail,name='video_detail'),
    path('post_list/',views.post_list,name='post_list'),
    path('post_detail/<int:pk>/',views.post_detail,name='post_detail'),

    ]