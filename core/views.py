from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from patients.models import Patient 
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Billing
from stock.models import Product, Movement  # import stock
from datetime import date, timedelta
from datetime import date, timedelta


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

    if getattr(user, "role", "") == "admin":
        stats["products"] = Product.objects.count()
        stats["movements"] = Movement.objects.count()

        seuil_stock = 50
        seuil_jours = 15
        today = date.today()

        # on récupère tous les produits et on filtre en Python
        produits = list(Product.objects.all())

        produits_stock_faible = [p for p in produits if p.current_stock < seuil_stock]

        produits_peremption_proche = [
            p for p in produits
            if p.expiration_date and p.expiration_date <= today + timedelta(days=seuil_jours)
        ]

        stats["produits_stock_faible"] = produits_stock_faible
        stats["produits_peremption_proche"] = produits_peremption_proche
        stats["alerts_count"] = len(produits_stock_faible) + len(produits_peremption_proche)

    return render(request, "core/dashboard.html", {"stats": stats})
