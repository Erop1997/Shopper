from django.urls import path
from . import views

urlpatterns = [
    path('admin/',views.admin, name='home'),
    path('order/<int:pk>',views.order, name='order'),
    path('edit_order_admin/<int:pk>', views.edit_order, name='edit_order_admin'),
]