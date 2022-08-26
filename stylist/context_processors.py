from django.contrib.sites.models import Site
from django.conf import settings
from .models import Style

# ---------------
# CONTEXT PROCESSOR
# ---------------

def add_rgb_colors(css_attrs):
    ## adds rgb values for all colors
    for key, value in settings.STYLE_SCHEMA.items():
        if value['type'] == 'color':
            hex = css_attrs[key].lstrip("#")
            css_attrs[f"{key}-rgb"] = ",".join(tuple(str(int(hex[i:i+2], 16)) for i in (0, 2, 4)))
    return css_attrs

def get_font_families(css_attrs):
    ## adds import strings for google fonts
    font_keys = [ key for key, value in settings.STYLE_SCHEMA.items() if value['type'] == 'font' ]
    font_import = ""
    for key in font_keys:
        font_import += f"&family={css_attrs[key].replace(' ', '+')}:wght@100;200;300;400;500;600;700;800;900"
    return font_import

def get_custom_styles(request):
    if getattr(request, "site", None):
        site = request.site
    else:
        site = Site.objects.get_current()
        
    try:
        css_attrs = Style.objects.filter(site=site).get(enabled=True).attrs
        custom_style = add_rgb_colors(css_attrs)
        custom_font_import = get_font_families(css_attrs)

    except:
        custom_style = None
        custom_font_import = None
    try:
        css_attrs = request.session.get("preview_css")
        preview_style = add_rgb_colors(css_attrs)
        preview_font_import = get_font_families(css_attrs)
    except:
        preview_style = None
        preview_font_import = None
    
    return {
        'custom_style': custom_style,
        'custom_font_import': custom_font_import,
        'preview_style': preview_style,
        'preview_font_import': preview_font_import
    }

