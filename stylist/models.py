import uuid
import sass
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.sites.models import Site
from django.utils.text import slugify

from autoslug import AutoSlugField
from tempfile import gettempdir

STYLIST_CSS_MEDIA_PATH = getattr(settings, "STYLIST_CSS_MEDIA_PATH", 'site/{domain}/style/{filename}')
STYLIST_DEFAULT_CSS = getattr(settings, "STYLIST_DEFAULT_CSS")
STYLIST_SCSS_TEMPLATE = getattr(settings, "STYLIST_SCSS_TEMPLATE")

def css_file_path(instance, filename):
    """
    Method sets up the path to save the CSS file to.
    """
    # return 'site/{domain}/style/{filename}'.format(context)

    context = { 'domain': instance.site.domain,      # Done this way so we can expose more varibles
                'filename': filename,
                'site_name': slugify(instance.site.name),
                'uuid': instance.uuid}

    return STYLIST_CSS_MEDIA_PATH.format(**context)

def default_attrs():
    attrs = {}
    for key in settings.STYLE_SCHEMA:
        attrs[key] = settings.STYLE_SCHEMA[key]["default"]
    return attrs


class Style(models.Model):
    """
    The model that holds all the variables for 
    """
    name = models.CharField(_("Name"), max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = AutoSlugField(verbose_name=_("Slug"), populate_from="name", unique_with=('site__id',), always_update=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True, related_name="site_style")        # Overwriting this field from Base Class to change the related_name
    attrs = models.JSONField(blank=True, default=default_attrs)
    enabled = models.BooleanField(_("Enabled"))
    css_file = models.FileField(_("CSS File"), upload_to=css_file_path, max_length=100, blank=True, null=True)                                 # Location where the Compiled CSS file is placed.  Used so a completely custom file can be uploaded.

    class Meta:
        verbose_name = _( "Site Style")
        verbose_name_plural = _( "Site Styles")

    def __str__(self):
        return "{}: {}".format(self.site.name, self.name)

    def get_absolute_url(self):
        return reverse( "stylist:stylist-edit", kwargs={"uuid": self.uuid})
    
    def get_style_css(self):
        if not self.css_file:
            return STYLIST_DEFAULT_CSS
        
        return self.css_file.url

    def compile_attrs(self):
        with open(gettempdir() + "/custom_vars.scss", "w+") as custom_vars:
            string = ""
            google_fonts = "@import url('https://fonts.googleapis.com/css2?family="
            num_fonts = 0
            for key in self.attrs:
                string += "$" + key + ": " + self.attrs[key] + ";\n"
                if settings.STYLE_SCHEMA[key]["type"] == "font":
                    if num_fonts > 0:
                        google_fonts += "&family="
                    google_fonts += self.attrs[key].replace(" ", "+")
                    google_fonts += ":wght@100;200;300;400;500;600;700;800;900"
                    num_fonts += 1
            if num_fonts > 0:
                google_fonts += "&display=swap');\n"
                string = google_fonts + string
            custom_vars.write(string)
            custom_vars.seek(0)

            content = sass.compile(filename=STYLIST_SCSS_TEMPLATE, include_paths=[gettempdir()])
            self.css_file.save(self.name + ".css", ContentFile(content.encode()))
            os.remove(custom_vars.name)


@receiver(post_save, sender=Style)
def only_one_active_style(sender, instance, **kwargs):
    if instance.enabled:
        Style.objects.filter(site=instance.site).exclude(pk=instance.pk).update(enabled=False)
