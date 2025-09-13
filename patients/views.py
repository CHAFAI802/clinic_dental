from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm

@login_required
def patient_list(request):
    patients = Patient.objects.filter(medecin=request.user)  # <--- filtre
    return render(request, "patients/patient_list.html", {"patients": patients})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "patients/patient_detail.html", {"patient": patient})


@login_required
def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.medecin = request.user  # <--- on attache le user connecté
            patient.save()
            return redirect("patients:patient_list")
        else:
            print("Erreurs de validation :", form.errors)
    else:
        form = PatientForm()
    return render(request, "patients/patient_form.html", {"form": form})

@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patients:patient_list")
    else:
        form = PatientForm(instance=patient)
    return render(request, "patients/patient_form.html", {"form": form})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        patient.delete()
        return redirect("patients:patient_list")
    return render(request, "patients/patient_confirm_delete.html", {"patient": patient})

