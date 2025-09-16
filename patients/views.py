# patients/views.py
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Patient
from .forms import PatientForm


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"
    paginate_by = 10

    def get_queryset(self):
        return Patient.objects.filter(medecin=self.request.user).order_by("last_name")



class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = "patients/patient_detail.html"
    context_object_name = "patient"

    def get_queryset(self):
        return Patient.objects.filter(medecin=self.request.user)


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"
    success_url = reverse_lazy("patients:patient_list")

    def form_valid(self, form):
        # Associer automatiquement le médecin connecté au patient
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
