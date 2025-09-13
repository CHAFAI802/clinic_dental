from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm 
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q


@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    return render(request, "appointments/appointment_list.html", {"appointments": appointments})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, "appointments/appointment_detail.html", {"appointment": appointment})

@login_required
def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = request.user
            appointment.save()
            return redirect("appointments:appointment_list")
    else:
        form = AppointmentForm()
    return render(request, "appointments/appointment_form.html", {"form": form})


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("appointments:appointment_list")
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, "appointments/appointment_form.html", {"form": form})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        return redirect("appointments:appointment_list")
    return render(request, "appointments/appointment_confirm_delete.html", {"appointment": appointment})


def recherche_ajax(request):
    q = request.GET.get("q", "")
    results = Appointment.objects.filter(
        Q(patient__nom__icontains=q) |  # adapte le champ selon ton modèle Patient
        Q(date__icontains=q)
    )

    html = render_to_string("appointments/resultats.html", {"results": results})
    return JsonResponse({"html": html})