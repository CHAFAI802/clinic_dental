from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from patients.models import Patient
from appointments.models import Appointment
from datetime import date, time

class DashboardViewTests(TestCase):
    def setUp(self):
        # Groupes
        self.admin_group = Group.objects.create(name="Admin")
        self.medecin_group = Group.objects.create(name="Médecin")
        self.secretaire_group = Group.objects.create(name="Secrétaire")

        # Utilisateurs
        self.admin_user = User.objects.create_user(username="admin", password="admin123")
        self.medecin_user = User.objects.create_user(username="medecin", password="medecin123")
        self.secretaire_user = User.objects.create_user(username="secretaire", password="secret123")

        # Assignation aux groupes
        self.admin_user.groups.add(self.admin_group)
        self.medecin_user.groups.add(self.medecin_group)
        self.secretaire_user.groups.add(self.secretaire_group)

        # Patient
        self.patient = Patient.objects.create(
            first_name="Ali", last_name="Ben Salah", date_of_birth="1990-05-10"
        )

        # Rendez-vous
        self.rdv = Appointment.objects.create(
            patient=self.patient,
            doctor=self.medecin_user,
            date=date.today(),
            time=time(10, 0),
            notes="Contrôle"
        )

    def test_admin_dashboard(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Total Patients")
        self.assertContains(response, "Total Rendez-vous")

    def test_medecin_dashboard(self):
        self.client.login(username="medecin", password="medecin123")
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vos rendez-vous")
        self.assertContains(response, "Ali Ben Salah")

    def test_secretaire_dashboard(self):
        self.client.login(username="secretaire", password="secret123")
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patients")
        self.assertContains(response, "Rendez-vous")

    def test_non_authenticated_redirect(self):
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 302)  # redirection login
