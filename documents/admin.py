from django.contrib import admin
from .models import DocumentTemplate, DynamicDocument

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'doc_type', 'created_by', 'created_at')
    search_fields = ('name', 'doc_type')


@admin.register(DynamicDocument)
class DynamicDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'created_by', 'created_at')
    readonly_fields = ('generated_html',)
    search_fields = ('template__name',)