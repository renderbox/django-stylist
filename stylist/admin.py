from django.contrib import admin

from .models import Style, Font


def compile_styles(modeladmin, request, queryset):
    for q in queryset:
        q.compile_attrs()
compile_styles.short_description = "Compile selected styles"


class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'site', 'attrs', 'enabled')
    list_filter = ('site', 'enabled')
    search_fields = ('name', 'slug')
    actions = [compile_styles]


class FontAdmin(admin.ModelAdmin):
    list_display = ('id', 'family', 'provider', 'preferred')
    list_filter = ('preferred',)
    search_fields = ('family',)

    
admin.site.register(Font, FontAdmin)
admin.site.register(Style, StyleAdmin)
