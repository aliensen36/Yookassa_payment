from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_order, name='create_order'),
    path('payment_success/', views.payment_success, name='payment_success'),
]
