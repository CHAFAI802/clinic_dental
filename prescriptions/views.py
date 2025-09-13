# prescriptions/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from .models import Prescription
from .forms import PrescriptionForm
from .utils import generate_prescription_pdf

@login_required
def create_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    prescription, created = Prescription.objects.get_or_create(appointment=appointment)

    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            # Redirige vers la vue PDF (ouvrira le PDF directement)
            return redirect("prescriptions:prescription_pdf", pk=appointment_id)
        
    else:
        form = PrescriptionForm(instance=prescription)

    return render(
        request,
        "prescriptions/create_prescription.html",
        {"form": form, "appointment": appointment},
    )




@login_required
def prescription_pdf(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    prescription = getattr(appointment, "prescription", None)

    return generate_prescription_pdf(
        appointment_id=pk,
        prescription_text=prescription.text if prescription else "some thing wrong"
    )
