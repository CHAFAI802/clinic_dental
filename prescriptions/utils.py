# prescriptions/utils.py
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from appointments.models import Appointment

def generate_prescription_pdf(appointment_id, prescription_text=""):
    appointment = Appointment.objects.get(id=appointment_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="ordonnance_{appointment.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # En-tête
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Ordonnance Médicale")

    # Infos patient
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Patient : {appointment.patient.first_name} {appointment.patient.last_name}")
    p.drawString(50, height - 120, f"Date : {appointment.date} à {appointment.time}")

    # Texte prescription
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 160, "Prescription :")
    p.drawString(50, height - 180, prescription_text if prescription_text else "Aucune prescription.")

    # Signature
    p.drawString(50, 100, f"Médecin : {appointment.doctor.last_name} *****{appointment.doctor.first_name}")

    p.showPage()
    p.save()

    return response
