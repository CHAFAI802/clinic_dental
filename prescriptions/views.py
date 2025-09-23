# prescriptions/views.py
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Prescription
from .forms import PrescriptionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
import io
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from appointments.models import Appointment 

class PatientPrescriptionsListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = "prescriptions/prescription_list.html"
    context_object_name = "prescriptions"
    paginate_by = 10

    def get_queryset(self):
        return Prescription.objects.filter(
            appointment__patient__medecin=self.request.user
        )


class PatientPrescriptionDetailView(LoginRequiredMixin, DetailView):
    model = Prescription
    template_name = 'prescriptions/prescription_detail.html'
    context_object_name = 'prescription'

    def get_queryset(self):
        return Prescription.objects.filter(
            appointment__medecin=self.request.user
        )

class PatientPrescriptionCreateView(LoginRequiredMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "prescriptions/prescription_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        appointment_id = self.kwargs.get("appointment_id")
        if not appointment_id and 'appointment' in form.fields:
            form.fields['appointment'].queryset = Appointment.objects.filter(medecin=self.request.user)
        return form
    

    def form_valid(self, form):
        appointment_id = self.kwargs.get("appointment_id")
        if appointment_id:
            # Cas où on a déjà un rendez-vous dans l'URL
            appointment = get_object_or_404(Appointment, pk=appointment_id, medecin=self.request.user)
            form.instance.prescription = appointment
        # sinon le champ appointment est rempli par l'utilisateur dans le formulaire
        return super().form_valid(form)

    def get_success_url(self):
        # redirection vers la liste des prescriptions du patient concerné
        return reverse('prescriptions:prescription_list')
    





class PatientPrescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescriptions/prescription_form.html'
    success_url = reverse_lazy('prescriptions:prescription_list')

    def get_queryset(self):
        return Prescription.objects.filter(
            appointment__medecin=self.request.user
        )


class PatientPrescriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Prescription
    template_name = "prescriptions/prescription_confirm_delete.html"
    success_url = reverse_lazy("prescriptions:prescription_list")

    def get_queryset(self):
        return Prescription.objects.filter(
            appointment__medecin=self.request.user
        )


@login_required
def generate_prescription_pdf(request, pk):
    """Génère un PDF pour une ordonnance Prescription donnée"""
    prescription = get_object_or_404(Prescription, pk=pk)

    # Contrôle d'accès : seul le médecin du patient peut voir
    if prescription.appointment.medecin != request.user:
        raise Http404("Vous n'avez pas accès à cette ordonnance")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --------- En-tête ----------
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "ORDONNANCE")

    # --------- Informations ----------
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Patient : {prescription.appointment.patient}")
    p.drawString(50, 730, f"Date RDV : {prescription.appointment.date}")
    p.drawString(50, 710, f"Texte : {prescription.text}")

    # --------- Pied de page ----------
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 50, "Cabinet Dentaire - Ordonnance générée automatiquement")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f"ordonnance_{prescription.id}.pdf"
    )
