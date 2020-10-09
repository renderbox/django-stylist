# import uuid 

# from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
# from django.urls import reverse
from django.contrib.sites.models import Site
from autoslug import AutoSlugField

class Style(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    slug = AutoSlugField(verbose_name=_("Slug"), populate_from="name", unique_with=('site__id',), always_update=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True, related_name="site_style")        # Overwriting this field from Base Class to change the related_name
    attrs = models.JSONField(blank=True, default=dict)
    enabled = models.BooleanField(_("Enabled"))

    class Meta:
        verbose_name = _( "Site Style")
        verbose_name_plural = _( "Site Styles")

    def __str__(self):
        return "{}: {}".format(self.site.name, self.name)

#     def get_absolute_url(self):
#         return reverse( "samplemodel_detail", kwargs={"uuid": self.uuid})
