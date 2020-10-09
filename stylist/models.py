import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
# from django.urls import reverse
from django.contrib.sites.models import Site
from django.utils.text import slugify

from autoslug import AutoSlugField

SASS_MEDIA_PATH = getattr(settings, "SASS_MEDIA_PATH", 'site/{domain}/style/{filename}')
SASS_DEFAULT_CSS = getattr(settings, "SASS_DEFAULT_CSS")

def css_file_path(instance, filename):
    """
    Method sets up the path to save the CSS file to.
    """
    # return 'site/{domain}/style/{filename}'.format(context)

    context = { 'domain': instance.site.domain,      # Done this way so we can expose more varibles
                'filename': filename,
                'site_name': slugify(instance.site.name),
                'uuid': instance.uuid}

    return SASS_MEDIA_PATH.format(context)

class Style(models.Model):
    """
    The model that holds all the variables for 
    """
    name = models.CharField(_("Name"), max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = AutoSlugField(verbose_name=_("Slug"), populate_from="name", unique_with=('site__id',), always_update=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True, related_name="site_style")        # Overwriting this field from Base Class to change the related_name
    attrs = models.JSONField(blank=True, default=dict)
    enabled = models.BooleanField(_("Enabled"))
    css_file = models.FileField(_("CSS File"), upload_to=css_file_path, max_length=100)                                 # Location where the Compiled CSS file is placed.  Used so a completely custom file can be uploaded.

    class Meta:
        verbose_name = _( "Site Style")
        verbose_name_plural = _( "Site Styles")

    def __str__(self):
        return "{}: {}".format(self.site.name, self.name)

#     def get_absolute_url(self):
#         return reverse( "stylist:edit", kwargs={"uuid": self.uuid})
    
    def get_style_css(self):
        if not attrs or css_file:
            return SASS_DEFAULT_CSS
        
        return self.css_file.url