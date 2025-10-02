from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription avec validation améliorée"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre.email@exemple.com',
            'autocomplete': 'email'
        }),
        label="Adresse email"
    )
    
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom',
            'autocomplete': 'given-name'
        }),
        label="Prénom"
    )
    
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom',
            'autocomplete': 'family-name'
        }),
        label="Nom"
    )
    
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="Rôle",
        initial="secretaire"
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'autocomplete': 'new-password'
        }),
        label="Mot de passe"
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe',
            'autocomplete': 'new-password'
        }),
        label="Confirmation du mot de passe"
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "role", "password1", "password2")

    def clean_email(self):
        """Vérifier que l'email n'existe pas déjà"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        return email.lower()

    def clean_first_name(self):
        """Capitaliser le prénom"""
        return self.cleaned_data.get('first_name').strip().capitalize()

    def clean_last_name(self):
        """Mettre le nom en majuscules"""
        return self.cleaned_data.get('last_name').strip().upper()


class CustomAuthenticationForm(AuthenticationForm):
    """Formulaire de connexion personnalisé"""
    
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre.email@exemple.com',
            'autocomplete': 'email',
            'autofocus': True
        }),
        label="Adresse email"
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'autocomplete': 'current-password'
        }),
        label="Mot de passe"
    )

    error_messages = {
        'invalid_login': "Email ou mot de passe incorrect.",
        'inactive': "Ce compte est inactif.",
    }


class PasswordResetRequestForm(forms.Form):
    """Formulaire de demande de réinitialisation"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre.email@exemple.com',
            'autocomplete': 'email'
        }),
        label="Adresse email"
    )