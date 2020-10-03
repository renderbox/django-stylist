from django.urls import path

from stylist import views

urlpatterns = [
    path("", views.StylistIndexView.as_view(), name="stylist-index"),
]
