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

from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        return Appointment.objects.filter(
            patient__medecin=self.request.user
        ).order_by("-date")

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("appointments:appointment_list")

    def form_valid(self, form):
        form.instance.medecin = self.request.user
        return super().form_valid(form)

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
