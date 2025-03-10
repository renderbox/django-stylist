from django.contrib.sites.models import Site

from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination


from stylist.models import Style, Font
from stylist.api.serializers import StyleSerializer, FontSerializer
from stylist.settings import app_settings


def create_style(request, serializer, name=None, attrs=None):
    if getattr(request, "site", None):
        site = request.site
    else:
        site = Site.objects.get_current()
    instance = serializer.save(site=site, name=name, attrs=attrs)

    if app_settings.USE_SASS:
        instance.compile_attrs()

    if not Style.objects.filter(site=site, enabled=True):
        instance.enabled = True
        instance.save()


class StyleCreateAPIView(CreateAPIView):
     queryset = Style.objects.all()
     serializer_class = StyleSerializer

     def perform_create(self, serializer):
        create_style(self.request, serializer)


class StyleDuplicateAPIView(CreateAPIView):
     queryset = Style.objects.all()
     serializer_class = StyleSerializer

     def perform_create(self, serializer):
        previous = Style.objects.get(uuid=self.kwargs["uuid"])
        new_name = previous.name + " copy"
        create_style(self.request, serializer, new_name, previous.attrs)


class FontPagination(PageNumberPagination):
    page_size = 20
    
class FontViewset(
   viewsets.ReadOnlyModelViewSet
):
    queryset = Font.objects.all()
    serializer_class = FontSerializer
    pagination_class = FontPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['family']