from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),
    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
]