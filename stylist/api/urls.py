from django.urls import path

from stylist.api import views

urlpatterns = [
    path('style/create/', views.StyleCreateAPIView.as_view(), name='api-create-style'),
    path('style/<uuid:uuid>/duplicate/', views.StyleDuplicateAPIView.as_view(), name='api-duplicate-style'),
]
