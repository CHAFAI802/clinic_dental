from pathlib import Path

def get_version():
    """
    Lit le fichier VERSION.txt à la racine du projet
    et renvoie la version sous forme de chaîne.
    """
    version_file = Path(__file__).resolve().parent.parent / "VERSION.txt"
    if version_file.exists():
        with open(version_file, "r", encoding="utf-8") as f:
            # Première ligne uniquement
            return f.readline().strip()
    return "Version inconnue"
