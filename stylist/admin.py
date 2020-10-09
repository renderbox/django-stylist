from django.contrib import admin

from .models import Style


class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'site', 'attrs', 'enabled')
    list_filter = ('site', 'enabled')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


admin.register(Style, StyleAdmin)