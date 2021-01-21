from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from stylist.models import Style

class StyleForm(forms.ModelForm):

    class Meta:
        model = Style
        fields = ["name", "enabled"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].initial = "New Theme"
        self.fields["enabled"].initial = False


class StyleEditForm(forms.ModelForm):
    class Meta:
        model = Style
        fields = ["name"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.instance.attrs:
            self.fields[key] = forms.CharField(required=True, label=settings.STYLE_SCHEMA[key]["label"])
            self.fields[key].initial = self.instance.attrs[key]

    def clean(self):
        cleaned_data = super().clean()
        for key in cleaned_data:
            if key != "name":
                if settings.STYLE_SCHEMA[key]["type"] == "color":
                    self.clean_color(key)
                elif settings.STYLE_SCHEMA[key]["type"] == "number":
                    self.clean_number(key)
                elif settings.STYLE_SCHEMA[key]["type"] == "rem":
                    self.clean_rem(key)
                elif settings.STYLE_SCHEMA[key]["type"] == "px":
                    self.clean_px(key)
        return cleaned_data

    # clean key types
    def clean_color(self, key):
        data = self.cleaned_data[key]
        if data[0] != "#":
            raise ValidationError("Please enter a valid hex code")
        return data

    def clean_number(self, key):
        data = self.cleaned_data[key]
        try:
            value = float(data)
        except:
            raise ValidationError("Please enter a valid number")
        return data

    def clean_rem(self, key):
        data = self.cleaned_data[key]
        try:
            # if it is a number, add rem to end of the string
            number = float(data)
            data += "rem"
            self.cleaned_data[key] = data
        except:
            try:
                # else check if the string is a number followed by "rem"
                value = float(data[:-3])
                if data[-3:] != "rem":
                    raise ValidationError("Please enter a valid rem value")
            except:
                raise ValidationError("Please enter a valid rem value")
        return data

    def clean_px(self, key):
        data = self.cleaned_data[key]
        try:
            # if it is a number, add px to the end of the string
            number = float(data)
            data += "px"
            self.cleaned_data[key] = data
        except:
            try:
                # else check if the string is a number followed by "px"
                value = float(data[:-2])
                if not data[-2:] == "px":
                    raise ValidationError("Please enter a valid px value")
            except:
                raise ValidationError("Please enter a valid px value")
        return data

    def save(self):
        instance = super().save()
        if self.changed_data:
            for field in self.changed_data:
                if field != "name": 
                    instance.attrs[field] = self.cleaned_data[field]
            if len(self.changed_data) > 0 or self.changed_data[0] != "name":
                instance.save()
                instance.compile_attrs()
        return instance
