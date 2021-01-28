from django.urls import path

from stylist import views

app_name = "stylist"

urlpatterns = [
    path("", views.StylistIndexView.as_view(), name="stylist-index"),
    path("style/<uuid:uuid>/edit/", views.StylistUpdateView.as_view(), name="stylist-edit"),
    path("style/<uuid:uuid>/preview/", views.StylistPreviewView.as_view(), name="stylist-preview"),
    path("style/<uuid:uuid>/delete/", views.StylistDeleteView.as_view(), name="stylist-delete"),
    path("style/active/", views.StylistActiveView.as_view(), name="stylist-make-active"),
    path("style/preview/end/", views.end_preview, name="stylist-end-preview"),
]
