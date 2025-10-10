import os
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Active ou désactive le bandeau d’environnement (SHOW_ENV_BANNER)."

    def add_arguments(self, parser):
        parser.add_argument(
            "state",
            type=str,
            choices=["on", "off"],
            help="État du bandeau : 'on' pour activer, 'off' pour désactiver.'"
        )

    def handle(self, *args, **options):
        state = options["state"].lower()

        # Localise correctement settings.py, même s’il est dans un sous-dossier
        settings_module_path = settings.SETTINGS_MODULE.replace('.', os.sep) + ".py"
        settings_path = Path(settings.BASE_DIR) / settings_module_path

        if not settings_path.exists():
            raise CommandError(f"Fichier settings.py introuvable à l’emplacement : {settings_path}")

        with open(settings_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        updated = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("SHOW_ENV_BANNER"):
                new_value = "True" if state == "on" else "False"
                new_lines.append(f"SHOW_ENV_BANNER = {new_value}\n")
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            new_value = "True" if state == "on" else "False"
            new_lines.append(f"\nSHOW_ENV_BANNER = {new_value}\n")

        with open(settings_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Bandeau d’environnement {'activé' if state == 'on' else 'désactivé'} avec succès."
        ))
