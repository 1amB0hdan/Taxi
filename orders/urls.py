from django.urls import path
from . import views  # Імпортуємо модуль views цілком, це захистить від ImportError!

urlpatterns = [
    # Головний дашборд водія/менеджера
    path('dashboard/', views.role_dashboard, name='role_dashboard'),
    
    # Створення замовлення з головної сторінки
    path('create/', views.create_order, name='create_order'),
    
    # Кнопки для зміни статусів замовлення водієм
    path('driver/take/<int:order_id>/', views.driver_take_order, name='driver_take_order'),
    path('driver/complete/<int:order_id>/', views.driver_complete_order, name='driver_complete_order'),
]