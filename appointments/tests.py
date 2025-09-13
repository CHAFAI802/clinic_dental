from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from patients.models import Patient
from appointments.models import Appointment

User = get_user_model()

class AppointmentViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="doc@example.com",
            password="test123",
            role="medecin"
        )
        self.client.login(email="doc@example.com", password="test123")

        self.patient = Patient.objects.create(
            first_name="Jean",
            last_name="Dupont",
            date_of_birth="1990-01-01",
            phone="0600000000",
            email="jean.dupont@example.com"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.user,
            date="2025-09-04",
            time="10:00:00"
        )

    def test_appointment_list_view(self):
        response = self.client.get(reverse("appointments:appointment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jean")

