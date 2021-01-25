from django.contrib.sites.models import Site
from django.shortcuts import reverse, redirect
from django.views.generic import FormView, ListView, UpdateView, DeleteView

from .forms import StyleForm, StyleEditForm, ActiveStyleForm
from .models import Style

class StylistIndexView(ListView):
    """
    List of styles available for editing
    """
    template_name = "stylist/index.html"
    model = Style

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["form"] = StyleForm
        context["active_form"] = ActiveStyleForm
        try:
            context["active_theme"] = Style.objects.filter(site=Site.objects.get_current()).get(enabled=True)
        except:
            pass
        return context


# Stylist Preview Link - Autogenerated CSS from SASS/SCSS


# Stylist Edit Page
class StylistUpdateView(UpdateView):
    model = Style
    form_class = StyleEditForm

    def get_object(self, *args, **kwargs):
        return Style.objects.get(uuid=self.kwargs.get("uuid"))


# Change which Style is currently active for the site
class StylistActiveView(FormView):
    form_class = ActiveStyleForm
    template_name = "stylist/active_form.html"

    def form_valid(self, form):
        instance = form.cleaned_data["active"]
        instance.enabled = True
        instance.save()
        return redirect('stylist:stylist-index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        try:
            context["active_theme"] = Style.objects.filter(site=Site.objects.get_current()).get(enabled=True)
        except:
            pass
        return context



# Stylist Detail Page


class StylistDeleteView(DeleteView):
    model = Style
    template_name = 'stylist/style_delete.html'

    def get_object(self, queryset=None):
        return Style.objects.get(uuid=self.kwargs.get("uuid"))

    def get_success_url(self):
        return reverse('stylist:stylist-index')
