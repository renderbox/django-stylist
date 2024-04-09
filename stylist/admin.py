from django.contrib import admin, messages
from django.conf import settings
from django.core.management import call_command

from .models import Style, Font
from .settings import app_settings
from .utils import get_font_families


def compile_styles(modeladmin, request, queryset):
    for q in queryset:
        q.compile_attrs()


compile_styles.short_description = "Compile selected styles"


def sync_google_fonts(modeladmin, request, queryset):
    if not hasattr(settings, "GOOGLE_WEBFONTS_KEY"):
        modeladmin.message_user(
            request,
            "Please set GOOGLE_WEBFONTS_KEY in your settings.py",
            messages.ERROR,
        )
        return None

    deleted, updates = get_font_families()

    modeladmin.message_user(
        request,
        f"Updated or Added {len(updates)} fonts",
        messages.SUCCESS,
    )
    modeladmin.message_user(
        request,
        f"DELETED fonts on in list {deleted}",
        messages.SUCCESS,
    )


sync_google_fonts.short_description = "Sync with google's font api"


class StyleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "site", "attrs", "enabled")
    list_filter = ("site", "enabled")
    search_fields = ("name", "slug")

    def __init__(self, model=Style, admin_site=admin.site) -> None:
        super().__init__(model, admin_site)
        if app_settings.USE_SASS:
            self.actions.append(compile_styles)


class FontAdmin(admin.ModelAdmin):
    list_display = ("id", "family", "provider", "preferred")
    list_filter = ("preferred",)
    search_fields = ("family",)

    actions = [sync_google_fonts]


admin.site.register(Font, FontAdmin)
admin.site.register(Style, StyleAdmin)
