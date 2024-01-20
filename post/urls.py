from django.urls import path, include
from .views import PlaceViewSet, PlaceDetailView
from rest_framework.routers import DefaultRouter
# My urls here.

router = DefaultRouter()
router.register('places', PlaceViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('detail/<int:id>/', PlaceDetailView.as_view()),

]