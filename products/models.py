from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='imgs/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Campos opcionales específicos según el producto
    size = models.CharField(max_length=10, blank=True, null=True)  # ej: S, M, L (para fajas)
    color = models.CharField(max_length=7, blank=True, null=True, help_text="Código hexadecimal del color (ej: #FF69B4)")

    def __str__(self):
        return self.name
