from. import views
from django.urls import path

urlpatterns = [
    path('registration/', views.register, name='registration'),
    path('log_in/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='logout'),
]