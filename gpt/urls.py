from django.urls import path, include
from . import views
app_name='gpt'

urlpatterns = [

    path('', views.chat_page, name='chat'),
    path('new/', views.new_chat, name='new_chat'),
    path('ask/', views.ask_gpt, name='ask'),
    path('delete/<int:session_id>/',views.delete_chat,name='delete_chat'),
    path('<int:session_id>/', views.chat_page, name='chat_session'),

]