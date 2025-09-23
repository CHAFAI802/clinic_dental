from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Patient
from .forms import PatientForm
from appointments.models import Appointment

# --- Patients ---
class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"
    paginate_by = 10

    def get_queryset(self):
        return Patient.objects.filter(medecin=self.request.user)
    
class PatientDetailView(LoginRequiredMixin, DetailView):
    model=Patient
    template_name='patients/patient_detail.html'
    context_object_name ='patient'
    
    def get_queryset(self):
        
        return Patient.objects.filter(medecin=self.request.user)



class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"
    success_url = reverse_lazy("patients:patient_list")

    def form_valid(self, form):
        form.instance.medecin = self.request.user
        return super().form_valid(form)

    

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"
    success_url = reverse_lazy("patients:patient_list")

    def get_queryset(self):
        return Patient.objects.filter(medecin=self.request.user)


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = "patients/patient_confirm_delete.html"
    success_url = reverse_lazy("patients:patient_list")

    def get_queryset(self):
        return Patient.objects.filter(medecin=self.request.user)


@method_decorator(login_required, name='dispatch')
class AppointmentToggleDoneView(View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        # optionnel: vérifier que le médecin connecté est bien propriétaire du patient
        if appointment.patient.medecin == request.user:
            appointment.done = not appointment.done
            appointment.save()
        return redirect('appointments:appointment_list')  

