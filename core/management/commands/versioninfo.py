from django.core.management.base import BaseCommand
from django.conf import settings
from core.utils import get_version

class Command(BaseCommand):
    help = "Affiche les informations de version et d’environnement du projet."

    def handle(self, *args, **options):
        version = get_version()
        environment = "Développement" if settings.DEBUG else "Production"
        show_banner = getattr(settings, "SHOW_ENV_BANNER", True)

        self.stdout.write(self.style.SUCCESS("📦 Informations du projet"))
        self.stdout.write(f"Version actuelle     : {version}")
        self.stdout.write(f"Environnement        : {environment}")
        self.stdout.write(f"Bandeau activé       : {'Oui' if show_banner else 'Non'}")
        self.stdout.write(f"DEBUG                : {'Oui' if settings.DEBUG else 'Non'}")
        self.stdout.write(f"Nom du projet Django : {settings.BASE_DIR.name}")
