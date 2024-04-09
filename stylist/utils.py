import requests
from django.conf import settings
from stylist.models import Font


def get_weights(variants):
    weights = []
    for el in variants:
        if el == "regular":
            weights.append("400")
        elif el.isnumeric():
            weights.append(el)
    return weights


def get_font_families():
    r = requests.get(
        url="https://www.googleapis.com/webfonts/v1/webfonts?key="
        + settings.GOOGLE_WEBFONTS_KEY
    )
    r.raise_for_status()

    items = r.json().get("items", {})
    ids = []
    font_tuples = []
    for item in items:
        family = item.get("family").strip()
        family_url = family.replace(" ", "+")
        defaults = {
            "href": f"https://fonts.googleapis.com/css2?family={family_url}:wght@100;200;300;400;500;600;700;800;900&display=swap",
            "weights": get_weights(item.get("variants", [])),
        }
        db_update = Font.objects.update_or_create(
                defaults=defaults,
                provider="google",
                family=family,
            )
        font_tuples.append(
            db_update
        )
        ids.append(db_update[0].pk)

    deleted = Font.objects.exclude(pk__in=ids).delete()
    
    return deleted, font_tuples
