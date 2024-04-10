import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from stylist.models import Font
from stylist.utils import get_font_families

def get_weights(variants):
    weights = []
    for el in variants:
        if el == "regular":
            weights.append("400")
        elif el.isnumeric():
            weights.append(el)
    return weights


class Command(BaseCommand):
    def handle(self, *args, **options):

        if not hasattr(settings, "GOOGLE_WEBFONTS_KEY"):
            self.stdout.write(self.style.ERROR("No Google Webfonts Key found"))
            return None

        deleted, db_updates = get_font_families()
        for font, created in db_updates:
            if created:
                self.stdout.write(self.style.SUCCESS(f"ADDED new font: {font}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated font: {font}"))

        self.stdout.write(self.style.SUCCESS(f"Deleted fonts not in list {deleted}"))
