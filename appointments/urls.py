from django.urls import path
from . import views
from .views import (
    AppointmentListView,
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentDetailView,
    AppointmentUpdateView,
)

app_name = "appointments"

urlpatterns = [
    path("", AppointmentListView.as_view(), name="appointment_list"),
    path("<int:pk>/", AppointmentDetailView.as_view(), name="appointment_detail"),
    path("add/", AppointmentCreateView.as_view(), name="appointment_create"),
    path("<int:pk>/presence/", views.confirm_presence, name="confirm_presence"),
    path("<int:pk>/edit/", AppointmentUpdateView.as_view(), name="appointment_update"),
    path("<int:pk>/delete/", AppointmentDeleteView.as_view(), name="appointment_delete"),
    path("recherche-ajax/", views.recherche_ajax, name="recherche_ajax"),
]
