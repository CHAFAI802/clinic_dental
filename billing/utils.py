import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Invoice

def generate_invoice_pdf(invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # En-tête
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "FACTURE")

    # Infos patient
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Patient : {invoice.patient}")
    p.drawString(50, 730, f"Date : {invoice.date}")
    p.drawString(50, 710, f"Montant : {invoice.amount} €")
    p.drawString(50, 690, f"Statut : {invoice.get_status_display()}")

    if invoice.amount:
        p.drawString(50, 670, f"Notes : {invoice.amount}")

    # Pied de page
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 50, "Cabinet Dentaire - Facturation Générée Automatiquement")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"facture_{invoice.id}.pdf")
