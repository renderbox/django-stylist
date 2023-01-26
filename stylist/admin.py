from django.contrib import admin

from .models import Style
from .settings import app_settings


def compile_styles(modeladmin, request, queryset):
    for q in queryset:
        q.compile_attrs()
compile_styles.short_description = "Compile selected styles"


class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'site', 'attrs', 'enabled')
    list_filter = ('site', 'enabled')
    search_fields = ('name', 'slug')
    
    def __init__(self, model=Style, admin_site=admin.site) -> None:
        super().__init__(model, admin_site)
        if app_settings.USE_SASS:
            self.actions.append(compile_styles)

admin.site.register(Style, StyleAdmin)
