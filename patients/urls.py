from django.urls import path
from .views import AppointmentToggleDoneView
from .views import(
    PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView, PatientDeleteView,AllPatientsListView
)

app_name = "patients"

urlpatterns = [
    path("", PatientListView.as_view(), name="patient_list"),
    path("add/", PatientCreateView.as_view(), name="patient_create"),
    path("<int:pk>/", PatientDetailView.as_view(), name="patient_detail"),
    path("<int:pk>/edit/", PatientUpdateView.as_view(), name="patient_update"),
    path("<int:pk>/delete/", PatientDeleteView.as_view(), name="patient_delete"),
    path("all/", AllPatientsListView.as_view(), name="all_patients"),
    
]


