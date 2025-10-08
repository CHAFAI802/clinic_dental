# prescriptions/views.py
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import PrescriptionForm,PrescriptionItemFormSet,PrescriptionItem,PrescriptionItemForm,Prescription
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .utils.prescription_pdf import draw_prescription
PrescriptionItemFormSet = inlineformset_factory(
    Prescription, PrescriptionItem, form=PrescriptionItemForm,
    extra=1, can_delete=True
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
import os
from .models import Prescription
from appointments.models import Appointment, Patient
from django.conf import settings 

# ================================
# LISTES DES PRESCRIPTIONS
# ================================

class PatientPrescriptionsListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = "prescriptions/prescription_list.html"
    context_object_name = "prescriptions"
    paginate_by = 10

    def get_queryset(self):
        return (Prescription.objects
                .filter(appointment__patient__medecin=self.request.user)
                .select_related("appointment")
                .order_by("-appointment__datetime"))


class PatientAllPrescriptionsListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = "prescriptions/patient_all_prescriptions.html"
    context_object_name = "prescriptions"
    paginate_by = 10

    def get_queryset(self):
        self.patient = get_object_or_404(Patient, pk=self.kwargs["pk"])
        return (Prescription.objects
                .filter(
                    appointment__patient=self.patient,
                    appointment__patient__medecin=self.request.user
                )
                .select_related("appointment")
                .order_by("-appointment__datetime"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = self.patient
        return context


# ================================
# DETAIL D’UNE PRESCRIPTION
# ================================

class PatientPrescriptionDetailView(LoginRequiredMixin, DetailView):
    model = Prescription
    template_name = 'prescriptions/prescription_detail.html'
    context_object_name = 'prescription'

    def get_queryset(self):
        return Prescription.objects.filter(
            appointment__patient__medecin=self.request.user
        )


# ================================
# CREATION / MODIFICATION / SUPPRESSION
# ================================
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PrescriptionItemFormSet(self.request.POST)
        else:
            context['formset'] = PrescriptionItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        appointment_id = self.kwargs.get("appointment_id")
        if appointment_id:
            appointment = get_object_or_404(Appointment, pk=appointment_id, medecin=self.request.user)
            form.instance.appointment = appointment

        self.object = form.save()  # on sauvegarde la prescription
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('prescriptions:patient_all_prescriptions', args=[self.object.appointment.patient.pk])




class PatientPrescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescriptions/prescription_form.html'

    def get_queryset(self):
        return (Prescription.objects
            .filter(appointment__patient__medecin=self.request.user)
            .select_related("appointment", "appointment__patient")
            .prefetch_related("items")
            .order_by("-appointment__date"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PrescriptionItemFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['formset'] = PrescriptionItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('prescriptions:patient_all_prescriptions', 
                      args=[self.object.appointment.patient.pk])

class PatientPrescriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Prescription
    template_name = "prescriptions/prescription_confirm_delete.html"

    def get_queryset(self):
        return Prescription.objects.filter(
            appointment__patient__medecin=self.request.user
        )

    def get_success_url(self):
        return reverse('prescriptions:patient_all_prescriptions', args=[self.object.appointment.patient.pk])


# ================================
# PDF
# ================================

@login_required
def prescription_pdf_view(request, pk):
    prescription = get_object_or_404(
        Prescription,
        pk=pk,
        appointment__patient__medecin=request.user
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ordonnance_{prescription.pk}.pdf"'

    c = canvas.Canvas(response, pagesize=A5)
    draw_prescription(c, prescription)
    c.showPage()
    c.save()

    return response