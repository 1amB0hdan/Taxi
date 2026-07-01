from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Очікується'),
        (STATUS_IN_PROGRESS, 'В дорозі'),
        (STATUS_COMPLETED, 'Виконано'),
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_orders',
        verbose_name='Клієнт'
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='driver_orders',
        verbose_name='Водій'
    )
    pickup_location = models.CharField(max_length=255, verbose_name='Звідки')
    dropoff_location = models.CharField(max_length=255, verbose_name='Куди')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')

    def __str__(self):
        return f"{self.client.username}: {self.pickup_location} → {self.dropoff_location}"
