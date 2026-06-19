from django.contrib import admin
from .models import UserProfile, Order, OrderNotification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone', 'is_verified', 'rating', 'created_at')
    list_filter = ('user_type', 'is_verified')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_display', 'driver_display', 'service_type', 'status', 'estimated_price', 'created_at')
    list_filter = ('status', 'service_type', 'created_at')
    search_fields = ('customer__email', 'customer__first_name', 'driver__email', 'pickup_location', 'dropoff_location')
    readonly_fields = ('created_at',)
    
    def customer_display(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"
    customer_display.short_description = 'Customer'
    
    def driver_display(self, obj):
        if obj.driver:
            return f"{obj.driver.first_name} {obj.driver.last_name}"
        return "-"
    driver_display.short_description = 'Driver'

@admin.register(OrderNotification)
class OrderNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'recipient_display', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__email', 'message')
    readonly_fields = ('created_at',)
    
    def recipient_display(self, obj):
        return f"{obj.recipient.first_name} {obj.recipient.last_name}"
    recipient_display.short_description = 'Recipient'
