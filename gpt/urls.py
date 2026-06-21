from django.urls import path, include
from . import views
app_name='gpt'

urlpatterns = [
    path('', views.chat_page, name='chat'),
path('ask/', views.ask_gpt, name='ask_gpt'),

    ]