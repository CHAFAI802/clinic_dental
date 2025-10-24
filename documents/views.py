# documents/views.py 
from django.http import JsonResponse, HttpResponse 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template, Context
from .models import DocumentTemplate, DynamicDocument
from .forms import DynamicDocumentForm 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import ListView 
import json 
import pdfkit 
from django.core.files.storage import default_storage
from django.conf import settings
import tempfile
import os






# documents/views.py
@login_required
def create_template(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        DocumentTemplate.objects.create(
            name=name,
            content=content,
            created_by=request.user
        )
        return redirect('documents:template_list')
    return render(request, 'documents/create_template.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        path = default_storage.save(f'uploads/{image.name}', image)
        image_url = os.path.join(settings.MEDIA_URL, path)
        return JsonResponse({'url': image_url})
    return JsonResponse({'error': 'Aucune image reçue'}, status=400)

@login_required
def delete_document(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id, created_by=request.user)
    template.delete()
    messages.success(request, "Le modèle a été supprimé avec succès.")
    return redirect('documents:template_list')


@csrf_exempt
def update_document(request, pk):
    """Met à jour le HTML du document avant génération du PDF."""
    if request.method == 'POST':
        data = json.loads(request.body)
        html_content = data.get('html', '')
        document = get_object_or_404(DynamicDocument, pk=pk)
        document.generated_html = html_content
        document.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405) 



from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import DocumentTemplate 

class DocumentTemplateListView(LoginRequiredMixin, ListView):
    model = DocumentTemplate
    template_name = "documents/template_list.html"
    context_object_name = "templates"

    def get_queryset(self):
        return DocumentTemplate.objects.filter(created_by=self.request.user)


class DocumentTemplateCreateView(CreateView):
    model = DocumentTemplate
    fields = ["name", "doc_type", "content"]
    template_name = "documents/template_form.html"
    success_url = reverse_lazy("documents:template_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


def document_preview(request, pk):
    document = get_object_or_404(DynamicDocument, pk=pk)
    return render(request, 'documents:create_document', {'document': document})



@csrf_exempt  # utile si tu veux tester sans problème de CSRF via fetch()
def generate_pdf(request):
    try:
        data = json.loads(request.body)
        html_content = data.get('html', '')
        if not html_content.strip():
            return JsonResponse({'error': 'Aucun contenu HTML reçu.'}, status=400)

        # Ajout d’un style de base pour PDF
        html_template = f"""
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{
              font-family: Arial, sans-serif;
              margin: 25px;
              color: #333;
            }}
            h1, h2, h3 {{
              color: #007bff;
            }}
            table {{
              width: 100%;
              border-collapse: collapse;
              margin-top: 15px;
            }}
            th, td {{
              border: 1px solid #ccc;
              padding: 8px;
              text-align: left;
            }}
            img {{
              max-width: 100%;
              height: auto;
            }}
            .qr {{
              text-align: center;
              margin-top: 20px;
            }}
          </style>
        </head>
        <body>
          {html_content}
        </body>
        </html>
        """

        # Chemin vers wkhtmltopdf
        wkhtmltopdf_path = getattr(settings, "WKHTMLTOPDF_PATH", None)
        options = {
            'enable-local-file-access': None,
            'quiet': '',
            'encoding': "UTF-8",
        }

        # Si wkhtmltopdf est configuré
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path) if wkhtmltopdf_path else None
        pdf = pdfkit.from_string(html_template, False, options=options, configuration=config)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="document.pdf"'
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)    
    

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import DocumentTemplate

@login_required
def template_list(request):
    templates = DocumentTemplate.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'documents/template_list.html', {'templates': templates})


@login_required
def edit_template(request, pk):
    template = get_object_or_404(DocumentTemplate, pk=pk, created_by=request.user)

    if request.method == 'POST':
        template.name = request.POST.get('name')
        template.content = request.POST.get('content')
        template.save()
        return redirect('documents:template_list')

    return render(request, 'documents:create_template', {'edit_mode': True, 'template': template})
