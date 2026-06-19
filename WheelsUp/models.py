from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPES = (
        ('customer', 'Заказчик'),
        ('driver', 'Водій'),
        ('admin', 'Адміністратор'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    rating = models.FloatField(default=5.0)  # Для водіїв
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_user_type_display()})"
    
    class Meta:
        verbose_name_plural = "User Profiles"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікується'),
        ('accepted', 'Прийнято'),
        ('in_progress', 'В дорозі'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_customer')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_as_driver')
    
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    dropoff_latitude = models.FloatField(null=True, blank=True)
    dropoff_longitude = models.FloatField(null=True, blank=True)
    
    service_type = models.CharField(
        max_length=20,
        choices=[
            ('economy', 'Economy'),
            ('comfort', 'Comfort'),
            ('premium', 'Premium'),
        ],
        default='economy'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    estimated_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.pickup_location} → {self.dropoff_location}"
    
    class Meta:
        ordering = ['-created_at']


class OrderNotification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.recipient.username} - Order #{self.order.id}"
    
    class Meta:
        ordering = ['-created_at']
