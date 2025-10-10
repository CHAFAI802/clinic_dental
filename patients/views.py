from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Patient
from .forms import PatientForm
from appointments.models import Appointment
from django.db.models import Q


# --- Patients ---
class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"
    paginate_by = 10

    def get_queryset(self):
        qs = Patient.objects.filter(medecin=self.request.user)
        q = self.request.GET.get("q")
        if q:
            # découpe la chaîne par espaces
            for term in q.split():
                qs = qs.filter(
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term) |
                    Q(phone__icontains=term) |
                    Q(email__icontains=term)
                )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context



    
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.request.user.is_medecin():
            form.instance.medecin = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.is_secretaire():
            return reverse_lazy("patients:all_patients")
        return reverse_lazy("patients:patient_list")
    
    
class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"
    success_url = reverse_lazy("patients:patient_list")

    def get_queryset(self):
        user = self.request.user
        if user.is_medecin():
            return Patient.objects.filter(medecin=user)
        elif user.is_secretaire() or user.is_admin():
            return Patient.objects.all()
        return Patient.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = "patients/patient_confirm_delete.html"
    success_url = reverse_lazy("patients:patient_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin():
            raise PermissionDenied("Seul un administrateur peut supprimer un patient.")
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class AppointmentToggleDoneView(View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        # optionnel: vérifier que le médecin connecté est bien propriétaire du patient
        if appointment.patient.medecin == request.user:
            appointment.done = not appointment.done
            appointment.save()
        return redirect('appointments:appointment_list')  






class AllPatientsListView(LoginRequiredMixin, ListView):
    """Liste de tous les patients, accessible seulement aux secrétaires et admins"""
    model = Patient
    template_name = "patients/all_patients.html"
    context_object_name = "patients"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        """Vérifie que l’utilisateur a le droit d’accès"""
        if not request.user.is_secretaire() and not request.user.is_admin():
            raise PermissionDenied("Vous n’avez pas accès à cette page.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Patient.objects.all()
        q = self.request.GET.get("q")
        if q:
            # découpe la chaîne par espaces
            for term in q.split():
                qs = qs.filter(
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term) |
                    Q(phone__icontains=term) |
                    Q(email__icontains=term)
                )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context
