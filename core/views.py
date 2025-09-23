from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from patients.models import Patient 
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Billing
from stock.models import Product, Movement  # import stock

@login_required
def dashboard_view(request):
    user = request.user
    patients = Patient.objects.filter(medecin=user)
    appointments = Appointment.objects.filter(patient__in=patients)
    prescriptions = Prescription.objects.filter(appointment__in=appointments)
    billings = Billing.objects.filter(appointment__in=appointments)

    stats = {
        "patients": patients.count(),
        "appointments": appointments.count(),
        "prescriptions": prescriptions.count(),
        "billings": billings.count(),
    }

    # Si admin, on ajoute le stock
    if getattr(user, "role", "") == "admin":
        stats["products"] = Product.objects.count()
        stats["movements"] = Movement.objects.count()

    return render(request, "core/dashboard.html", {"stats": stats})


