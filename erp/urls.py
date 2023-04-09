from django.urls import path
from . import views

app_name = 'erp'

urlpatterns = [
    path('', views.home, name='home'),
    path('product-create/', views.product_create, name='product-create'),
    path('product-list/', views.product_list, name='product-list'),
    path('inbound-create/', views.inbound_create, name='inbound-create'),
]
