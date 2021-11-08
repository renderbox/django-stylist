import os
import sass

from django.conf import settings
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
        
        custom_vars = build_scss(self, data)
        
        content = sass.compile(filename=settings.STYLIST_SCSS_TEMPLATE, include_paths=[gettempdir()])
        default_storage.delete(settings.STYLIST_DEFAULT_CSS)
        css_file = default_storage.save(settings.STYLIST_DEFAULT_CSS, ContentFile(content.encode()))

        os.remove(custom_vars.name)
        
        return 'build_scss: Wrote default css file ' + css_file
