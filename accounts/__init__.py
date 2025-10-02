# accounts/__init__.py
default_app_config = 'accounts.apps.AccountsConfig'


# accounts/apps.py
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Gestion des utilisateurs'
    
    def ready(self):
        """
        Méthode appelée lorsque l'application est prête
        Utilisée pour importer les signaux si nécessaire
        """
        pass