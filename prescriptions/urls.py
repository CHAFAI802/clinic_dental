from django.urls import path
from .views import (
    PatientPrescriptionsListView,
    PatientPrescriptionDetailView,
    PatientPrescriptionCreateView,
    PatientPrescriptionUpdateView,
    PatientPrescriptionDeleteView,
    generate_prescription_pdf,
)

app_name = "prescriptions"

urlpatterns = [
    # liste de toutes les ordonnances du médecin connecté
    path("", PatientPrescriptionsListView.as_view(), name="prescription_list"),

    # détail d’une ordonnance
    path("<int:pk>/", PatientPrescriptionDetailView.as_view(), name="prescription_detail"),

    # création d’une ordonnance : à adapter si tu passes l’ID du rendez-vous
    
    path('<int:pk>/create/', PatientPrescriptionCreateView.as_view(), name='prescription_create'),

        # modification d’une ordonnance
    path("<int:pk>/edit/", PatientPrescriptionUpdateView.as_view(), name="prescription_edit"),

    # suppression d’une ordonnance
    path("<int:pk>/delete/", PatientPrescriptionDeleteView.as_view(), name="prescription_delete"),

    # génération d’un PDF pour une ordonnance
    path("<int:pk>/pdf/", generate_prescription_pdf, name="prescription_pdf"),
]
