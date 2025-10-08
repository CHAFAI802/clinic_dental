from .models import ClinicInfo
from core.utils import get_version
from django.conf import settings

def clinic_settings(request):
    """Injecte les informations du cabinet dans tous les templates."""
    clinic_info = ClinicInfo.objects.first()
    theme_mode = request.session.get("theme_mode", None)

    if not clinic_info:
        return {"clinic_info": None, "theme_mode": theme_mode or "light"}

    # Priorité à la session utilisateur si elle existe
    if theme_mode:
        dark_mode = theme_mode == "dark"
    else:
        dark_mode = getattr(clinic_info, "dark_mode_enabled", False)

    return {
        "clinic_info": clinic_info,
        "theme_mode": "dark" if dark_mode else "light",
    }

def version_context(request):
    return {"version": get_version()}


def environment_context(request):
    """
    Indique dans quel environnement tourne le projet (dev / prod).
    """
    if settings.DEBUG:
        env = "Développement"
        color = "#0d6efd"  # bleu
    else:
        env = "Production"
        color = "#198754"  # vert

    return {"environment_name": env, "environment_color": color}