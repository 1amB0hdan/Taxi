from django.urls import path
from .views import (
    register_admin_view,
    register_customer_view,
    register_driver_view,
    register_view,
    login_view,
    logout_view,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register/customer/', register_customer_view, name='register_customer'),
    path('register/driver/', register_driver_view, name='register_driver'),
    path('register/admin/', register_admin_view, name='register_admin'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]
