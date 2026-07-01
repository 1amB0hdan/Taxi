from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CLIENT = 'client'
    ROLE_DRIVER = 'driver'
    ROLE_MANAGER = 'manager'

    ROLE_CHOICES = (
        (ROLE_CLIENT, 'Клієнт'),
        (ROLE_DRIVER, 'Водій'),
        (ROLE_MANAGER, 'Менеджер'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CLIENT)

    def is_client(self):
        return self.role == self.ROLE_CLIENT

    def is_driver(self):
        return self.role == self.ROLE_DRIVER

    def is_manager(self):
        return self.role == self.ROLE_MANAGER
