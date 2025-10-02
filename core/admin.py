# core/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import ClinicInfo

@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview')
    fields = ('name', 'logo', 'logo_preview')  # champs visibles dans le formulaire admin
    readonly_fields = ('logo_preview',)  # pas modifiable

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:60px;" />', obj.logo.url)
        return "(Aucun logo)"
    logo_preview.short_description = "Aperçu du logo"
