from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from .models import Billing
from .forms import BillingForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import io
from django.http import FileResponse, Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Billing  
import csv
from django.db.models import Q , Sum


# billing/views.py
class BillingListView(LoginRequiredMixin, ListView):
    model = Billing
    template_name = 'billing/billing_list.html'
    context_object_name = 'billings'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        # Vue de base
        qs = Billing.objects.all().order_by("-issued_at")

        # Restriction pour les médecins
        if getattr(user, "role", None) == "medecin":
            qs = qs.filter(appointment__medecin=user)

        # récupération des filtres GET
        nom_patient = self.request.GET.get("q", "").strip()
        date_facture = self.request.GET.get("datetime", "").strip()
        paid = self.request.GET.get("paid", "").strip()

        # Filtres facultatifs
        if nom_patient:
            qs = qs.filter(appointment__patient__last_name__icontains=nom_patient)

        if date_facture:
            qs = qs.filter(issued_at__date=date_facture)

        if paid in ["0", "1"]:
            qs = qs.filter(paid=bool(int(paid)))

        return qs

    def get_template_names(self):
        user = self.request.user
        if getattr(user, "role", None) in ["admin", "secretaire"]:
            return ["billing/all_factures.html"]
        return ["billing/billing_list.html"]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # renvoyer les valeurs saisies pour les garder dans le formulaire
        context["q"] = self.request.GET.get("q", "")
        context["datetime"] = self.request.GET.get("datetime", "")
        context["paid"] = self.request.GET.get("paid", "")
        return context

# export CSV séparé (même filtres)
class BillingExportCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # on reprend la logique de get_queryset
        qs = Billing.objects.filter(
            appointment__patient__medecin=self.request.user
        ).order_by("-issued_at")

        nom_patient = request.GET.get("q", "").strip()
        date_facture = request.GET.get("date", "").strip()
        paid = request.GET.get("paid", "").strip()

        if nom_patient:
            qs = qs.filter(appointment__patient__last_name__icontains=nom_patient)
        if date_facture:
            qs = qs.filter(issued_at__date=date_facture)
        if paid in ["0", "1"]:
            qs = qs.filter(paid=bool(int(paid)))

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="factures.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Patient", "Montant", "Payée", "Date émission"])
        for b in qs:
            writer.writerow([
                b.id,
                str(b.appointment.patient),
                b.amount,
                "Oui" if b.paid else "Non",
                b.issued_at.strftime("%d/%m/%Y"),
            ])
        return response   

class BillingDetailView(LoginRequiredMixin, DetailView):
    model = Billing
    template_name = 'billing/billing_detail.html'
    context_object_name = 'billing'

    def get_queryset(self):
        user = self.request.user

        if getattr(user, "role", None) in ["admin", "secretaire"]:
            return Billing.objects.all()

        # Médecin : seulement ses factures
        return Billing.objects.filter(appointment__medecin=user)



class BillingCreateView(LoginRequiredMixin, CreateView):
    model = Billing
    form_class = BillingForm
    template_name = 'billing/billing_form.html'
    success_url = reverse_lazy('billing:billing_list')


class BillingUpdateView(LoginRequiredMixin, UpdateView):
    model = Billing
    form_class = BillingForm
    template_name = 'billing/billing_form.html'
    success_url = reverse_lazy('billing:billing_list')


class BillingDeleteView(LoginRequiredMixin, DeleteView):
    model = Billing
    template_name = "billing/billing_confirm_delete.html"
    success_url = reverse_lazy("billing:billing_list")

    def get_queryset(self):
        # Empêcher de supprimer une facture qui ne lui appartient pas
        return Billing.objects.filter(appointment__patient__medecin=self.request.user)


@method_decorator(login_required, name='dispatch')
class BillingTogglePaidView(View):
    def post(self, request, pk):
        billing = get_object_or_404(
            Billing, pk=pk,
            appointment__patient__medecin=request.user  # sécurité
        )
        billing.paid = not billing.paid
        billing.save()
        return redirect('billing:billing_list')


@login_required
def generate_billing_pdf(request, pk):
    """Génère un PDF pour une facture Billing donnée"""
    billing = get_object_or_404(Billing, pk=pk)

    # (optionnel) : contrôler que l'utilisateur est bien le médecin du patient
    if billing.appointment.patient.medecin != request.user:
        raise Http404("Vous n'avez pas accès à cette facture")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --------- En-tête ----------
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "FACTURE")

    # --------- Informations ----------
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Patient : {billing.appointment.patient}")
    p.drawString(50, 730, f"Date RDV : {billing.appointment.date}")
    p.drawString(50, 710, f"Montant : {billing.amount} €")
    p.drawString(50, 690, f"Payée : {'Oui' if billing.paid else 'Non'}")

    # --------- Pied de page ----------
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 50, "Cabinet Dentaire - Facturation Générée Automatiquement")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"facture_{billing.id}.pdf")