from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from patients.models import Patient
from django.contrib.auth import get_user_model
from appointments.models import Appointment
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(nom="Test", prenom="Patient")
        self.medecin = CustomUser.objects.create_user(
            email="doc@test.com",
            password="Test1234!",
            role="medecin"
        )
        self.date = timezone.now().date()

    def test_appointment_in_past_not_allowed(self):
        rdv = Appointment(
            patient=self.patient,
            medecin=self.medecin,
            date=(timezone.now() - timedelta(days=1)).date(),
            time=(timezone.now() - timedelta(hours=1)).time()
        )
        with self.assertRaises(ValidationError):
            rdv.full_clean()

    def test_appointment_conflict_within_15_minutes(self):
        # Premier rendez-vous
        Appointment.objects.create(
            patient=self.patient,
            medecin=self.medecin,
            date=self.date,
            time=(timezone.now() + timedelta(minutes=30)).time()
        )
        # Deuxième dans les 10 minutes -> doit échouer
        rdv2 = Appointment(
            patient=self.patient,
            medecin=self.medecin,
            date=self.date,
            time=(timezone.now() + timedelta(minutes=40)).time()
        )
        with self.assertRaises(ValidationError):
            rdv2.full_clean()

    def test_appointment_conflict_respected(self):
        # Premier rendez-vous
        Appointment.objects.create(
            patient=self.patient,
            medecin=self.medecin,
            date=self.date,
            time=(timezone.now() + timedelta(minutes=30)).time()
        )
        # Deuxième à +20 minutes -> doit passer
        rdv2 = Appointment(
            patient=self.patient,
            medecin=self.medecin,
            date=self.date,
            time=(timezone.now() + timedelta(minutes=50)).time()
        )
        try:
            rdv2.full_clean()  # ne doit pas lever d'erreur
        except ValidationError:
            self.fail("Le rendez-vous espacé de 20 minutes ne devrait pas être rejeté.")
