# Application Accounts - Documentation

## 📋 Vue d'ensemble

L'application `accounts` gère l'authentification et la gestion des utilisateurs pour le système de cabinet dentaire.

## 🗂️ Structure des fichiers

```
accounts/
├── __init__.py
├── apps.py
├── admin.py                 # Interface d'administration
├── models.py                # Modèle CustomUser
├── forms.py                 # Formulaires d'inscription et connexion
├── views.py                 # Vues pour l'authentification
├── urls.py                  # Routes de l'application
├── migrations/              # Migrations de base de données
└── templates/
    └── accounts/
        ├── home.html
        ├── login.html
        ├── register.html
        ├── logout_confirm.html
        ├── password_reset.html
        ├── password_reset_confirm.html
        ├── password_reset_complete.html
        ├── password_reset_email.txt
        ├── password_reset_email.html
        ├── password_reset_subject.txt
        └── verification_sent.html
```

## 🔧 Configuration dans settings.py

```python
INSTALLED_APPS = [
    # ...
    'accounts',
    # ...
]

# Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'accounts.CustomUser'

# Configuration email (pour réinitialisation mot de passe)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # ou votre serveur SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre.email@exemple.com'
EMAIL_HOST_PASSWORD = 'votre_mot_de_passe'
DEFAULT_FROM_EMAIL = 'Cabinet Dentaire <noreply@votrecabinet.com>'

# Redirection après connexion/déconnexion
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:home'
```

## 📊 Modèle CustomUser

### Champs disponibles

- `email` : Identifiant unique (remplace username)
- `first_name` : Prénom
- `last_name` : Nom
- `role` : Rôle (medecin, secretaire, admin)
- `is_active` : Compte actif
- `is_staff` : Accès à l'admin Django
- `is_superuser` : Super utilisateur
- `date_joined` : Date d'inscription

### Méthodes utiles

```python
user.get_full_name()       # Retourne "Prénom NOM"
user.get_short_name()      # Retourne "Prénom"
user.is_medecin()          # True si médecin
user.is_secretaire()       # True si secrétaire
user.is_admin_user()       # True si admin ou superuser
```

## 🔐 Routes disponibles

| URL | Nom | Description |
|-----|-----|-------------|
| `/accounts/` | `accounts:home` | Page d'accueil |
| `/accounts/register/` | `accounts:register` | Inscription |
| `/accounts/login/` | `accounts:login` | Connexion |
| `/accounts/logout/` | `accounts:logout` | Déconnexion |
| `/accounts/password-reset/` | `accounts:password_reset` | Demande de réinitialisation |
| `/accounts/password-reset/sent/` | `accounts:verification_sent` | Confirmation d'envoi |
| `/accounts/password-reset/<uidb64>/<token>/` | `accounts:password_reset_confirm` | Formulaire nouveau MDP |
| `/accounts/password-reset/complete/` | `accounts:password_reset_complete` | Confirmation finale |

## 🎨 Formulaires

### CustomUserCreationForm
- Inscription avec email, prénom, nom, rôle et mot de passe
- Validation de l'unicité de l'email
- Nettoyage automatique des données (capitalisation, etc.)

### CustomAuthenticationForm
- Connexion avec email et mot de passe
- Messages d'erreur personnalisés

## 🚀 Utilisation

### Créer un utilisateur en code

```python
from accounts.models import CustomUser

# Utilisateur normal
user = CustomUser.objects.create_user(
    email='medecin@example.com',
    password='motdepasse123',
    first_name='Jean',
    last_name='DUPONT',
    role='medecin'
)

#