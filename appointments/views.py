from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
import json
from django.core.serializers.json import DjangoJSONEncoder



class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        q = self.request.GET.get("q", "")

        if user.role == "medecin":
            queryset = Appointment.objects.filter(patient__medecin=user)
        elif user.role in ["secretaire", "admin"]:
            queryset = Appointment.objects.all()
        else:
            queryset = Appointment.objects.none()

        if q:
            queryset = queryset.filter(
                Q(patient__first_name__icontains=q) |
                Q(patient__last_name__icontains=q) |
                Q(medecin__first_name__icontains=q) |
                Q(medecin__last_name__icontains=q) |
                Q(datetime__icontains=q)
            )

        return queryset.order_by("-datetime")

    def get_template_names(self):
        user = self.request.user
        if user.role == "medecin":
            return ["appointments/appointment_list.html"]
        elif user.role in ["secretaire", "admin"]:
            return ["appointments/all_appointments.html"]
        else:
            return ["appointments/appointment_list.html"]


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("appointments:appointment_list")


    def get_form_kwargs(self):
        """Injecter l’utilisateur dans le form pour appliquer la logique de rôle."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """
        Sécurisation :
        - on ignore le champ medecin qui vient du navigateur
        - on force le medecin lié au patient choisi
        """
        patient = form.cleaned_data.get("patient")
        if patient and patient.medecin:
            form.instance.medecin = patient.medecin
        else:
            # cas extrême : patient sans médecin affecté → on bloque
            form.add_error("patient", "Ce patient n'a pas de médecin assigné.")
            return self.form_invalid(form)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user=self.request.user
        if user.role=="medecin":
            patients=Patient.objects.filter(medecin=user)
        else:
            patients=Patient.objects.all()

        
        patients_data = {
            
            p.id: {
                "name": f"{p.first_name} {p.last_name}",
                "phone": p.phone,
                "email": p.email,
                "medecin": f"{p.medecin.last_name}" if p.medecin else None,
                "medecin_id": p.medecin.id if p.medecin else None, 
            }
            for p in patients
        }
        

        context["patients_json"] = json.dumps(patients_data, cls=DjangoJSONEncoder)
        q = self.request.GET.get("q", "")
        if q:
            filtered_appointments = Appointment.objects.filter(
                patient__first_name__icontains=q
            ) | Appointment.objects.filter(
                patient__last_name__icontains=q
            )
            context["appointments"] = filtered_appointments.order_by("-datetime")
        else:
            # Par défaut, les rendez-vous visibles selon rôle
            if user.role == "medecin":
                context["appointments"] = Appointment.objects.filter(patient__medecin=user).order_by("-datetime")
            else:
                context["appointments"] = Appointment.objects.all().order_by("-datetime")

        return context


    
class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return Appointment.objects.filter(patient__medecin=self.request.user)

class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("appointments:appointment_list")

    def get_queryset(self):
        return Appointment.objects.filter(patient__medecin=self.request.user)

class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = "appointments/appointment_confirm_delete.html"
    success_url = reverse_lazy("appointments:appointment_list")

    def get_queryset(self):
        return Appointment.objects.filter(patient__medecin=self.request.user)

@method_decorator(login_required, name='dispatch')
class AppointmentToggleDoneView(View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if appointment.patient.medecin == request.user:
            appointment.done = not appointment.done
            appointment.save()
        return redirect('appointments:appointment_list')

def recherche_ajax(request):
    q = request.GET.get("q", "")
    results = Appointment.objects.filter(
    Q(patient__first_name__icontains=q) |
    Q(patient__last_name__icontains=q) |
    Q(date__icontains=q)
)

    html = render_to_string("appointments/resultats.html", {"results": results})
    return JsonResponse({"html": html})
