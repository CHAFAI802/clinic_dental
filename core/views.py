from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from patients.models import Patient
from accounts.models import CustomUser
@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.groups.filter(name="Admin").exists():
        context["name"] = "Admin"
        context["patients_count"] = Patient.objects.count()
        context["appointments_count"] = Appointment.objects.count()

    elif user.groups.filter(name="Médecin").exists():
        context["name"] = "Médecin"
        context["appointments"] = Appointment.objects.filter(doctor=user)

    elif user.groups.filter(name="Secrétaire").exists():
        context["name"] = "Secrétaire"
        context["patients"] = Patient.objects.all()
        context["appointments"] = Appointment.objects.all()

    else:
        context["name"] = "Utilisateur"

    return render(request, "core/dashboard.html", context)

