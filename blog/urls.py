from django.urls import path
from . import views
app_name='blog'


urlpatterns = [
    path('',views.index,name='index'),
    # path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path("products/", views.product_list, name="product_list"),
    path("products/category/<int:category_id>/", views.product_list, name="product_list_by_category"),
    path("product_detail/<int:p_id>/", views.product_detail, name="product_detail"),
    path("cart_add/<int:p_id>/", views.cart_add, name="cart_add"),
    path("cart/", views.cart_list, name="cart_list"),
    path("cart/update/<int:p_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:p_id>/", views.cart_remove, name="cart_remove"),


    ]