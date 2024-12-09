from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),

    # Product Management
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),  # Product Detail URL
    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

    # Cart Management
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-history/', views.order_history, name='order_history'),


    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
