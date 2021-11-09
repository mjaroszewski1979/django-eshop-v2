from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('become_vendor/', views.become_vendor, name='become_vendor'),
    path('vendor_admin/', views.vendor_admin, name='vendor_admin'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_vendor/', views.edit_vendor, name='edit_vendor'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='vendor/login.html'), name='login'),
    path('', views.vendors, name='vendors'),
    path('<int:vendor_id>/', views.vendor, name='vendor')
]