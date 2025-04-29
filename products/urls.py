from django.urls import path, include
from rest_framework import routers
from products import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryView, 'categories')
router.register(r'products', views.ProductView, 'products')

urlpatterns = [
    path("api/", include(router.urls))
]