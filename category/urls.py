from django.urls import path, include
from .views import CategoryViewSet
from rest_framework.routers import DefaultRouter
# My urls here.

router = DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]