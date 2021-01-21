from django.urls import path

from stylist import views

app_name = "stylist"

urlpatterns = [
    path("", views.StylistIndexView.as_view(), name="stylist-index"),
    path("style/<uuid:uuid>/edit/", views.StylistUpdateView.as_view(), name="stylist-edit"),
    path("style/<uuid:uuid>/delete/", views.StylistDeleteView.as_view(), name="stylist-delete"),
]
