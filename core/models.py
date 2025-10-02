from django.db import models
from django.core.exceptions import ValidationError

class ClinicInfo(models.Model):
    name = models.CharField("Nom du cabinet", max_length=255)
    address = models.CharField("Adresse", max_length=255, blank=True)
    phone = models.CharField("Téléphone", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    logo = models.ImageField("Logo du cabinet", upload_to="clinic_logos/", blank=True, null=True)
    slogan = models.CharField(max_length=255,blank=True)
    
    primary_color = models.CharField("Couleur principale", max_length=7, default="#0d6efd")  
    secondary_color = models.CharField("Couleur secondaire", max_length=7, default="#6c757d") 
    background_color = models.CharField("Couleur de fond", max_length=7, default="#ffffff")   

    class Meta:
        verbose_name = "Information du cabinet"
        verbose_name_plural = "Informations du cabinet"

    def clean(self):
        # Empêche d'avoir plus d'un enregistrement
        if not self.pk and ClinicInfo.objects.exists():
            raise ValidationError("Il ne peut y avoir qu'une seule ligne d'informations du cabinet")

    def __str__(self):
        return self.name
