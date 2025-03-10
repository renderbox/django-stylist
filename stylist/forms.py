import re

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured

from .models import Style
from .settings import app_settings

class StyleForm(forms.ModelForm):

    class Meta:
        model = Style
        fields = ["name", "enabled"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].initial = "New Theme"
        self.fields["enabled"].initial = False


class ActiveStyleForm(forms.Form):
    active = forms.ModelChoiceField(queryset=Style.objects.all(), label="New Active Theme", empty_label="Choose Theme")

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)      
        site = settings.SITE_ID
        if hasattr(self, 'request') and hasattr(self.request, 'site'):
            site = self.request.site.id
        self.fields["active"].queryset = Style.objects.filter(site=site)
        try:
            self.fields["active"].initial = Style.objects.filter(site=site).get(enabled=True)
        except:
            pass



class StyleEditForm(forms.ModelForm):
    class Meta:
        model = Style
        fields = ["name"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.instance.attrs:
            self.fields[key] = forms.CharField(
                required=True,
                label=settings.STYLE_SCHEMA.get(key, {}).get("label", ""),
                widget=forms.TextInput(
                    attrs={'data-type': settings.STYLE_SCHEMA.get(key, {}).get("type", "")}
                )
            )
            self.fields[key].initial = self.instance.attrs[key]

    def clean(self):
        cleaned_data = super().clean()
        for key in list(cleaned_data):
            data_type = settings.STYLE_SCHEMA.get(key, {}).get("type", "")
            if key != "name":
                if data_type == "color":
                    self.clean_color(key)
                elif data_type == "number":
                    self.clean_number(key)
                elif data_type == "rem":
                    self.clean_rem(key)
                elif data_type == "px":
                    self.clean_px(key)
        
        if app_settings.USE_SASS:
            try:
                import sass
            except ModuleNotFoundError as err:
                self.add_error(None, ImproperlyConfigured("Improperly Configured: Please reinstall django-stylist with `pip install django-stylist[sass]` to add sass support"))

        return cleaned_data

    # clean key types
    def clean_color(self, key):
        data = self.cleaned_data[key]
        # match hex codes of length 3, 6, or 8
        match = re.match("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}|[A-Fa-f0-9]{8})$", data)
        if not match:
            self.add_error(key, ValidationError("Please enter a valid hex code"))
        return data

    def clean_number(self, key):
        data = self.cleaned_data[key]
        try:
            value = float(data)
        except:
            self.add_error(key, ValidationError("Please enter a valid number"))
        return data

    def clean_rem(self, key):
        data = self.cleaned_data[key]
        try:
            # if it is a number, add rem to end of the string
            float(data)
            data += "rem"
            self.cleaned_data[key] = data
        except:
            try:
                # else check if the string is a number followed by "rem"
                float(data[:-3])
                if data[-3:] != "rem":
                    self.add_error(key, ValidationError("Please enter a valid rem value"))
            except:
                self.add_error(key, ValidationError("Please enter a valid rem value"))
        return data

    def clean_px(self, key):
        data = self.cleaned_data[key]
        try:
            # if it is a number, add px to the end of the string
            float(data)
            data += "px"
            self.cleaned_data[key] = data
        except:
            try:
                # else check if the string is a number followed by "px"
                float(data[:-2])
                if not data[-2:] == "px":
                    self.add_error(key, ValidationError("Please enter a valid px value"))
            except:
                self.add_error(key, ValidationError("Please enter a valid px value"))
        return data

    def save(self):
        instance = super().save()
        if self.changed_data:
            for field in self.changed_data:
                if field != "name": 
                    instance.attrs[field] = self.cleaned_data[field]
            if len(self.changed_data) > 1 or self.changed_data[0] != "name":
                instance.save()
                if app_settings.USE_SASS:
                    instance.compile_attrs()
        return instance
