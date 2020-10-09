from django.urls import path

from stylist import views

app_name = "stylist"

urlpatterns = [
    path("", views.StylistIndexView.as_view(), name="stylist-index"),
]
