from .models import ClinicInfo

def clinic_info(request):
    """Ajoute les infos du cabinet dans tous les templates"""
    info = ClinicInfo.objects.first()  # retourne None si vide
    return {"clinic_info": info}
