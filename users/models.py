from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    ROL_CHOICES = (
        ('administrador', 'Administrador'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')

    USERNAME_FIELD = 'email'              
    REQUIRED_FIELDS = ['username']       

    def __str__(self):
        return self.email