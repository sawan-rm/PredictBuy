from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserViewSet, UserInteractionViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'users', UserViewSet, basename='user')
router.register(r'interactions', UserInteractionViewSet, basename='interaction')

urlpatterns = [
    path('', include(router.urls)),
]