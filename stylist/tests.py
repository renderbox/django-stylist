import os

from io import StringIO

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage
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
        self.user = get_user_model().objects.create(username="testuser")
        self.client.force_login(self.user)
    
    def test_style_creation_api(self):
        try:
            self.assertEquals(Style.objects.all().count(), 0)
            url = reverse("api-create-style")
            response = self.client.post(url, {"name": "Test", "enabled": "False"}, follow=True)
            self.assertEquals(Style.objects.all().count(), 1)
            
            style = Style.objects.get(pk=1)
            # since it's the only style, it should be enabled
            self.assertEquals(style.enabled, True)

            site = Site.objects.get_current()
            self.assertEquals(style.site, site)
            css_path = settings.MEDIA_ROOT + "/site/" + site.domain + "/style/Test.css"
            self.assertEquals(style.css_file.path, css_path)
            # remove the new file, leaving any preexisting files
            if(os.path.exists(css_path)):
                os.remove(css_path)
        except:
            print("")
            print(response.status_code)
            print(response.content.decode('utf-8'))
            raise

    def test_style_update(self):
        try:
            site = Site.objects.get_current()
            style = Style.objects.create(name="Test", enabled=False, site=site)
            url = reverse("stylist:stylist-edit", kwargs={"uuid": style.uuid})
            
            data = style.attrs
            data["name"] = "Updated"
            data["primary"] = "#FF0000"
            response = self.client.post(url, data, follow=True)

            style.refresh_from_db()
            self.assertEquals(style.name, "Updated")
            self.assertEquals(style.attrs["primary"], "#FF0000")
            
            css_path = settings.MEDIA_ROOT + "/site/" + site.domain + "/style/Updated.css"
            # remove the new file, leaving any preexisting files
            if(os.path.exists(css_path)):
                os.remove(css_path)
            
        except:
            print("")
            print(response.status_code)
            print(response.content.decode('utf-8'))
            raise

    def test_style_delete(self):
        try:
            style = Style.objects.create(name="Test", enabled=True)
            self.assertEquals(Style.objects.all().count(), 1)
            
            url = reverse("stylist:stylist-delete", kwargs={"uuid": style.uuid})
            response = self.client.post(url, follow=True)

            self.assertEquals(Style.objects.all().count(), 0)
        except:
            print("")
            print(response.status_code)
            print(response.content.decode('utf-8'))
            raise

    def test_style_active(self):
        try:
            site = Site.objects.get_current()
            style = Style.objects.create(name="Test", enabled=False, site=site)
            url = reverse("stylist:stylist-make-active")

            response = self.client.post(url, {"active": 1}, follow=True)
            self.assertEquals(response.context["active_theme"], style)
        except:
            print("")
            print(response.status_code)
            print(response.content.decode('utf-8'))
            raise


    def test_style_preview(self):
        try:
            site = Site.objects.get_current()
            style = Style.objects.create(name="Test", enabled=False, site=site)

            url = reverse("stylist:stylist-preview", kwargs={"uuid": style.uuid})
            data = style.attrs
            data["name"] = style.name
            response = self.client.post(url, data, follow=True)
            self.assertIn(settings.MEDIA_URL + "site/" + site.domain + "/style/Test_preview.css", response.context["preview_style"])

            # cleanup preview file
            path = self.client.session["preview_path"]
            default_storage.delete(path)
        except:
            print("")
            print(response.status_code)
            print(response.content.decode('utf-8'))
            raise


    def test_end_preview(self):
        try:
            site = Site.objects.get_current()
            style = Style.objects.create(name="Test", enabled=False, site=site)

            url = reverse("stylist:stylist-preview", kwargs={"uuid": style.uuid})
            data = style.attrs
            data["name"] = style.name
            response = self.client.post(url, data, follow=True)

            new_url = reverse("stylist:stylist-end-preview")
            new_response = self.client.get(new_url, HTTP_REFERER=reverse("stylist:stylist-index"), follow=True)
            self.assertEquals(new_response.context.get("preview_style"), None)
        except:
            print("")
            print(response.status_code)
            print(response.content.decode('utf-8'))
            raise


    def test_style_duplicate(self):
        try:
            site = Site.objects.get_current()
            style = Style.objects.create(name="Test", enabled=False, site=site)
            self.assertEquals(Style.objects.all().count(), 1)
            
            url = reverse("api-duplicate-style", kwargs={"uuid": style.uuid})
            response = self.client.post(url, {"name": style.name, "enabled": False}, follow=True)

            self.assertEquals(Style.objects.all().count(), 2)
            new_style = Style.objects.all().last()
            self.assertEquals(new_style.name, "Test copy")
            self.assertEquals(new_style.attrs, style.attrs)
        except:
            print("")
            print(response.status_code)
            print(response.content.decode('utf-8'))
            raise
