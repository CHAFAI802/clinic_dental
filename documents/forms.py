# documents/forms.py
from django import forms
from .models import DocumentTemplate, DynamicDocument
import re

class DynamicDocumentForm(forms.ModelForm):
    class Meta:
        model = DynamicDocument
        fields = ['template']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        template = self.initial.get('template') or self.instance.template
        if template:
            variables = re.findall(r"{{\s*(\w+)\s*}}", template.content)
            for var in variables:
                self.fields[var] = forms.CharField(label=var.replace('_', ' ').capitalize())
