import os
from django.conf import settings
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import cm
from reportlab.lib import colors

def draw_prescription(c, prescription):
    """
    Dessine l'ordonnance sur le canvas ReportLab c.
    """
    # --- 1. Logo ---
    if settings.DEBUG:
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'mountazeh.png')
    else:
        logo_path = os.path.join(settings.STATIC_ROOT, 'img', 'mountazeh.png')

    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo introuvable à {logo_path}")

    width, height = A5

    # Bande bleue
    c.setFillColor(colors.lightblue)
    c.rect(0, height - 3*cm, width, 3*cm, fill=1, stroke=0)
    c.setFillColor(colors.black)

    # Logo
    c.drawImage(logo_path, x=1*cm, y=height - 2.5*cm,
                width=2*cm, height=2*cm, preserveAspectRatio=True, mask='auto')

    # Texte bande
    medecin = prescription.appointment.medecin
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.white)
    c.drawString(4*cm, height - 1.3*cm, "Cabinet Médical")
    c.setFont("Helvetica", 9)
    c.drawString(4*cm, height - 2.1*cm,
                 f"Dr {medecin.first_name} {medecin.last_name} - {medecin.email} - Tél : 00 00 00 00")
    c.setFillColor(colors.black)

    # Titre
    c.setStrokeColor(colors.darkblue)
    c.line(1*cm, height - 4*cm, width - 1*cm, height - 4*cm)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(1*cm, height - 4.7*cm, "                    ORDONNANCE MÉDICALE                 ")

    # Patient / Date
    c.setFont("Helvetica", 10)
    c.drawString(1*cm, height - 6*cm, f"Patient : {prescription.appointment.patient}")
    c.drawString(1*cm, height - 6.7*cm,
                 f"Date du rendez-vous : {prescription.appointment.datetime.strftime('%d/%m/%Y %H:%M')}"
                )

    # Texte
    if prescription.text:
        c.setFont("Helvetica", 10)
        c.drawString(50, 480, "")
        text_object = c.beginText(50, 460)
        text_object.setFont("Helvetica", 10)
        text_object.textLines(prescription.text)
        c.drawText(text_object)

    # Médicaments
    y = 420
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "")
    y -= 20
    c.setFont("Helvetica", 10)

    for item in prescription.items.all():
        ligne = f"- {item.medicament} : {item.posologie} – {item.quantite} {item.unite}"
        c.drawString(50, y, ligne)
        y -= 15
        if y < 50:  # saut de page
            c.showPage()
            y = 750
            c.setFont("Helvetica", 10)

    # Pied de page
    c.setStrokeColor(colors.lightgrey)
    c.line(1*cm, 3*cm, width - 1*cm, 3*cm)
    c.setFont("Helvetica", 9)
    c.drawString(1*cm, 2.4*cm, "Fait à : _____________")
    c.drawString(1*cm, 1.9*cm, f"Le : {prescription.appointment.datetime.strftime('%d/%m/%Y %H:%M')}")
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(width - 6*cm, 1.5*cm, "Signature et cachet du médecin")
