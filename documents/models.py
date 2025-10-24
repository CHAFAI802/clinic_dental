# documents/models.py
from django.db import models
from django.conf import settings 
from django.utils import timezone

class DocumentTemplate(models.Model):
    DOC_TYPES = [
        ('billing', 'Facture'),
        ('prescription', 'Ordonnance'),
        ('attestation', 'Attestation'),
    ]
    name = models.CharField(max_length=100)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)
    content = models.TextField(help_text="HTML avec variables ex: {{ patient_name }}, {{ amount }}")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_doc_type_display()})"


class DynamicDocument(models.Model):
    template = models.ForeignKey(DocumentTemplate, on_delete=models.CASCADE)
    context_data = models.JSONField(default=dict)  # Variables dynamiques
    generated_html = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id} - {self.template.name}"

