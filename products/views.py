from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category

# Create your views here.
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
