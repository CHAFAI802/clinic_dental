from django.urls import path
from . import views

app_name = "patients"

urlpatterns = [
    path("", views.patient_list, name="patient_list"),
    path("<int:pk>/", views.patient_detail, name="patient_detail"),
    path("add/", views.patient_create, name="patient_create"),
    path("<int:pk>/edit/", views.patient_update, name="patient_update"),
    path("<int:pk>/delete/", views.patient_delete, name="patient_delete"),
    #path("<int:pk>/prescription/", views.prescription_pdf, name="prescription_pdf"),  # ➕ Ordonnance PDF
]
