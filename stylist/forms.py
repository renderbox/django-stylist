from django.forms import ModelForm

from stylist.models import Style

class StyleForm(ModelForm):

    class Meta:
        model = Style
        fields = ["name", "enabled"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].initial = "New Theme"
        self.fields["enabled"].initial = False
