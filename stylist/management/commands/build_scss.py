import os

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from tempfile import gettempdir

from stylist.views import build_scss

class Command(BaseCommand):
    def handle(self, *args, **options):        
        data = {}
        for key, entry in settings.STYLE_SCHEMA.items():
            data[key] = entry['default']
        try:
            import sass
        except ModuleNotFoundError as err:
            raise Exception("Please reinstall django-stylist with `pip install django-stylist[sass]` to add sass support") from err
        
        custom_vars = build_scss(self, data)
        
        content = sass.compile(filename=settings.STYLIST_SCSS_TEMPLATE, include_paths=[gettempdir()])
        
        if settings.STATIC_ROOT:
            file_storage = staticfiles_storage
        else:
            file_storage = default_storage
        file_storage.delete(settings.STYLIST_DEFAULT_CSS)
        css_file = file_storage.save(settings.STYLIST_DEFAULT_CSS, ContentFile(content.encode()))

        os.remove(custom_vars.name)
        
        return 'build_scss: Wrote default css file ' + css_file
