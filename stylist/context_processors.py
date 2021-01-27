from django.contrib.sites.models import Site

from .models import Style

# ---------------
# CONTEXT PROCESSOR
# ---------------


def get_custom_styles(request):
    if getattr(request, "site", None):
        site = request.site
    else:
        site = Site.objects.get_current()
        
    try:
        style = Style.objects.filter(site=site).get(enabled=True)
        custom_style = style.css_file.url
    except:
        custom_style = None

    preview = request.session.get("preview_css")

    return {
        'custom_style': custom_style,
        'preview_style': preview,
        }

