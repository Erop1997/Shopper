from django.urls import path
from . import views 

urlpatterns = [
    path('home/', views.home, name='home'),
    path('product/<int:pk>', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('guest_reg/<int:pk>', views.guest_reg, name='guest_reg'),
    path('create_order/', views.create_order, name='create_order'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('orders/', views.orders, name='orders'),
    path('favorite/', views.favorite, name='favorite'),
    path('edit_order/<int:pk>', views.edit_order, name='edit_order'),
]

