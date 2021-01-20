import os

from io import StringIO

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from stylist.models import Style

# Create your tests here.
class ModuleTests(TestCase):
    '''
    Tests to make sure basic elements are not missing from the package
    '''
    def test_for_missing_migrations(self):
        output = StringIO()

        try:
            call_command('makemigrations', interactive=False, dry_run=True, check=True, stdout=output)

        except SystemExit as e:
            # The exit code will be 1 when there are no missing migrations
            try:
                assert e == '1'
            except:
                self.fail("\n\nHey, There are missing migrations!\n\n %s" % output.getvalue())


class StylistClientTests(TestCase):
    '''
    Client tests for Stylist and the Style model
    '''
    def setUp(self):
        self.client = Client()
    
    def test_style_creation_api(self):
        try:
            self.assertEquals(Style.objects.all().count(), 0)
            url = reverse("api-create-style")
            response = self.client.post(url, {"name": "Test", "enabled": "False"}, follow=True)
            self.assertEquals(Style.objects.all().count(), 1)
            
            style = Style.objects.get(pk=1)
            # since it's the only style, it should be enabled
            self.assertEquals(style.enabled, True)
            self.assertEquals(style.site, Site.objects.get_current())

            css_path = settings.MEDIA_ROOT + "/site/example.com/style/Test.css"
            self.assertEquals(style.css_file, css_path)
            # remove the new file, leaving any preexisting files
            if(os.path.exists(css_path)):
                os.remove(css_path)
        except:
            print("")
            print(response.status_code)
            print(response.content.decode('utf-8'))
            raise
