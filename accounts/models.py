from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role="secretaire", **extra_fields):
        """Créer un utilisateur normal"""
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Créer un superutilisateur"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, role="admin", **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé avec email comme identifiant"""
    
    ROLE_CHOICES = [
        ("medecin", "Médecin"),
        ("secretaire", "Secrétaire"),
        ("admin", "Administrateur"),
    ]

    email = models.EmailField(unique=True, verbose_name="Adresse email")
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Nom")
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default="secretaire",
        verbose_name="Rôle"
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Date d'inscription")
    activation_sent_at = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']

    def __str__(self):
        return self.get_full_name() or self.email

    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Retourne le prénom de l'utilisateur"""
        return self.first_name or self.email.split('@')[0]

    def is_medecin(self):
        """Vérifie si l'utilisateur est un médecin"""
        return self.role == "medecin"

    def is_secretaire(self):
        """Vérifie si l'utilisateur est une secrétaire"""
        return self.role == "secretaire"

    def is_admin(self):
        """Vérifie si l'utilisateur est un administrateur"""
        return self.role == "admin" or self.is_superuser