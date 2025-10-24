from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from patients.models import Patient 
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Billing
from datetime import date, timedelta
from django.contrib.auth.decorators import user_passes_test
from .forms import ClinicInfoForm
from .models import ClinicInfo
from django.contrib import messages
from stock.models import Product, Movement
from django.views.generic import ListView
from .models import ActionLog
from django.contrib.auth.mixins import LoginRequiredMixin




@login_required
def dashboard_view(request):
    user = request.user
    context = {"role": None, "stats": {}}

    # --- Admin ---
    if user.is_admin():
        context["role"] = "Admin"

        patients = Patient.objects.all()
        appointments = Appointment.objects.all()
        prescriptions = Prescription.objects.all()
        billings = Billing.objects.all()

        context["patients"] = patients
        context["appointments"] = appointments
        context["prescriptions"] = prescriptions
        context["billings"] = billings

        context["stats"] = {
            "patients": patients.count(),
            "appointments": appointments.count(),
            "prescriptions": prescriptions.count(),
            "billings": billings.count(),
            "products": Product.objects.count(),
            "movements": Movement.objects.count(),
        }

        # Gestion du stock
        seuil_stock = 50
        seuil_jours = 15
        today = date.today()

        produits = list(Product.objects.all())
        produits_stock_faible = [p for p in produits if p.current_stock < seuil_stock]
        produits_peremption_proche = [
            p for p in produits
            if p.expiration_date and p.expiration_date <= today + timedelta(days=seuil_jours)
        ]

        context["stats"]["produits_stock_faible"] = produits_stock_faible
        context["stats"]["produits_peremption_proche"] = produits_peremption_proche
        context["stats"]["alerts_count"] = len(produits_stock_faible) + len(produits_peremption_proche)

    # --- Médecin ---
    elif user.is_medecin():
        context["role"] = "Médecin"
        patients = Patient.objects.filter(medecin=user)
        appointments = Appointment.objects.filter(medecin=user)
        prescriptions = Prescription.objects.filter(appointment__in=appointments)
        billings = Billing.objects.filter(appointment__in=appointments)

        context["patients"] = patients
        context["appointments"] = appointments
        context["prescriptions"] = prescriptions
        context["billings"] = billings

        context["stats"] = {
            "patients": patients.count(),
            "appointments": appointments.count(),
            "prescriptions": prescriptions.count(),
            "billings": billings.count(),
        }

    # --- Secrétaire ---
    elif user.is_secretaire():
        context["role"] = "Secrétaire"
        patients = Patient.objects.all()
        appointments = Appointment.objects.all()
        billings = Billing.objects.all()

        context["patients"] = patients
        context["appointments"] = appointments
        context["billings"] = billings

        context["stats"] = {
            "patients": patients.count(),
            "appointments": appointments.count(),
            "billings": billings.count(),
        }

    return render(request, "core/dashboard.html", context)


# Exemple d'utilisation en décorateur (si besoin sur d'autres vues admin-only)
def is_admin(user):
    return user.is_authenticated and user.role == "admin"
@login_required
def clinic_info_update(request):
    if request.user.role != 'admin':
        messages.error(request, "Accès réservé à l’administrateur.")
        return redirect('/')

    clinic_info, _ = ClinicInfo.objects.get_or_create(pk=1)
    if request.method == 'POST':
        form = ClinicInfoForm(request.POST, request.FILES, instance=clinic_info)
        if form.is_valid():
            form.save()
            messages.success(request, "Paramètres du cabinet mis à jour avec succès.")
            return redirect('core:clinic_info_update')
    else:
        form = ClinicInfoForm(instance=clinic_info)

    context = {
        'form': form,
        'clinic_info': clinic_info,
        'preview_style': {
            'background_color': clinic_info.background_color,
            'primary_color': clinic_info.primary_color,
            'secondary_color': clinic_info.secondary_color,
            'font_family': clinic_info.font_family,
        }
    }
    return render(request, 'core/clinic_info_form.html', context)


@login_required
def clinic_preview(request):
    """Page de prévisualisation dynamique du thème du cabinet."""
    if request.user.role != 'admin':
        messages.error(request, "Accès réservé à l’administrateur.")
        return redirect('/')

    clinic_info = ClinicInfo.objects.first()
    if not clinic_info:
        messages.warning(request, "Aucune information de cabinet trouvée.")
        return redirect('core:clinic_info_update')

    return render(request, 'core/clinic_preview.html', {
        'clinic_info': clinic_info
    })



def toggle_theme(request):
    """Bascule entre le mode clair et sombre."""
    current = request.session.get("theme_mode", "light")
    request.session["theme_mode"] = "dark" if current == "light" else "light"
    return redirect(request.META.get("HTTP_REFERER", "/"))




class ActionLogListView(LoginRequiredMixin, ListView):
    model = ActionLog
    template_name = "core/action_logs.html"
    context_object_name = "logs"
    ordering = ["-horodatage"]
