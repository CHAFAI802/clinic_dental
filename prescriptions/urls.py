# prescriptions/urls.py
from django.urls import path
from . import views

app_name = 'prescriptions'

urlpatterns = [
    path(
        "appointment/<int:appointment_id>/prescription/",
        views.create_prescription,
        name="create_prescription",
    ),
    path(
        "appointment/<int:pk>/prescription/pdf/",
        views.prescription_pdf,
        name="prescription_pdf",
    ),
]
