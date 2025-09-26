from django.urls import path
from .views import (
    PatientPrescriptionsListView,
    PatientPrescriptionDetailView,
    PatientPrescriptionCreateView,
    PatientPrescriptionUpdateView,
    PatientPrescriptionDeleteView,
    prescription_pdf_view,
    PatientAllPrescriptionsListView
)

app_name = "prescriptions"

urlpatterns = [
    # liste de toutes les ordonnances du médecin connecté
    path("", PatientPrescriptionsListView.as_view(), name="prescription_list"),

    # liste des ordonnances d’un patient précis
    path(
        "patient/<int:pk>/all/",
        PatientAllPrescriptionsListView.as_view(),
        name="patient_all_prescriptions"
    ),

    # détail d’une ordonnance
    path("<int:pk>/", PatientPrescriptionDetailView.as_view(), name="prescription_detail"),

    # création d’une ordonnance liée à un rendez-vous donné
    path(
        "appointment/<int:appointment_id>/create/",
        PatientPrescriptionCreateView.as_view(),
        name="prescription_create"
    ),

    # modification d’une ordonnance
    path("<int:pk>/edit/", PatientPrescriptionUpdateView.as_view(), name="prescription_edit"),

    # suppression d’une ordonnance
    path("<int:pk>/delete/", PatientPrescriptionDeleteView.as_view(), name="prescription_delete"),

    # génération d’un PDF pour une ordonnance
    path("<int:pk>/pdf/", prescription_pdf_view, name="prescription_pdf"),
]
