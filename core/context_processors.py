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


def environment_banner_context(request):
    """
    Rend le bandeau d'environnement disponible sur le site public,
    visible uniquement pour les administrateurs connectés.
    """
    if not request.user.is_authenticated or getattr(request.user, "role", "") != "admin":
        return {}

    from django.conf import settings
    env_name = "Développement" if settings.DEBUG else "Production"
    env_color = "#0d6efd" if settings.DEBUG else "#198754"

    return {
        "show_env_banner": True,
        "env_name": env_name,
        "env_color": env_color,
    }
