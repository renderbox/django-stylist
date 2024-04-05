import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from stylist.models import Font


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

        r = requests.get(
            url="https://www.googleapis.com/webfonts/v1/webfonts?key="
            + settings.GOOGLE_WEBFONTS_KEY
        )
        r.raise_for_status()

        items = r.json().get("items", {})
        ids = []
        for item in items:
            family = item.get("family").strip()
            family_url = family.replace(" ", "+")
            defaults = {
                "href": f"https://fonts.googleapis.com/css2?family={family_url}:wght@100;200;300;400;500;600;700;800;900&display=swap",
                "weights": get_weights(item.get("variants", [])),
            }

            font, created = Font.objects.update_or_create(
                defaults=defaults,
                provider="google",
                family=family,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"ADDED new font: {family}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated font: {family}"))

            ids.append(font.id)

        deleted = Font.objects.exclude(id__in=ids).delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted fonts not in list {deleted}"))
