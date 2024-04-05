from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stylist.api import views
router = DefaultRouter()
router.register(r'fonts', views.FontViewset, basename='font')
urlpatterns = [
    path("", include(router.urls)),
    path('style/create/', views.StyleCreateAPIView.as_view(), name='api-create-style'),
    path('style/<uuid:uuid>/duplicate/', views.StyleDuplicateAPIView.as_view(), name='api-duplicate-style'),
]
