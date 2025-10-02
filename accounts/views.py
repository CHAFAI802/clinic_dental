from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from .utils import account_activation_token
from .models import CustomUser
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


@sensitive_post_parameters('password1', 'password2')
@never_cache
def register(request):
    if request.user.is_authenticated:
        messages.info(request, "Vous êtes déjà connecté.")
        return redirect("core:dashboard")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # compte désactivé jusqu'à confirmation
            user.save()
            user.activation_sent_at = timezone.now()
            user.save()
            # Préparer email d’activation
            current_site = get_current_site(request)
            subject = "Activez votre compte"
            message = render_to_string("accounts/activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # expéditeur
                [user.email],
                fail_silently=False,
            )


            messages.success(
                request,
                "Votre compte a été créé. Vérifiez votre boîte mail pour confirmer votre adresse."
            )
            return redirect("accounts:login")
        else:
            messages.error(request, "Erreur lors de l'inscription.")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user:
        # Vérifier expiration (24h ici)
        if user.activation_sent_at and timezone.now() > user.activation_sent_at + timedelta(hours=24):
            messages.error(request, "Le lien d’activation a expiré. Demandez un nouvel email.")
            return redirect("accounts:resend_activation")

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Votre compte a été activé. Vous pouvez maintenant vous connecter.")
            return redirect("accounts:login")

    messages.error(request, "Lien d’activation invalide ou expiré.")
    return redirect("accounts:login")

from django.contrib.auth.forms import AuthenticationForm

def resend_activation(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Aucun compte n'est associé à cet email.")
            return redirect("accounts:resend_activation")

        if user.is_active:
            messages.info(request, "Ce compte est déjà activé. Vous pouvez vous connecter.")
            return redirect("accounts:login")

        # Ré-envoi de l'email d'activation
        current_site = get_current_site(request)
        subject = "Réactivation de votre compte"
        message = render_to_string("accounts/activation_email.html", {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        })
        send_mail(subject, message, None, [user.email])

        messages.success(request, "Un nouvel email d'activation a été envoyé.")
        return redirect("accounts:login")

    return render(request, "accounts/resend_activation.html")


@sensitive_post_parameters('password')
@never_cache
def login_view(request):
    """
    Vue de connexion
    Redirige vers le dashboard si l'utilisateur est déjà connecté
    """
    if request.user.is_authenticated:
        messages.info(request, "Vous êtes déjà connecté.")
        return redirect("core:dashboard")
    
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Spécifier explicitement le backend pour éviter l'erreur avec django-axes
            login(request, user, )
            messages.success(request, f"Bienvenue {user.first_name} !")
            
            # Redirection vers la page demandée ou dashboard par défaut
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:dashboard')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    """
    Vue de déconnexion
    Nécessite une confirmation via POST pour éviter les déconnexions accidentelles
    """
    if request.method == "POST":
        user_name = request.user.first_name or "utilisateur"
        logout(request)
        messages.success(request, f"Au revoir {user_name} ! Vous avez été déconnecté avec succès.")
        return redirect("accounts:home")
    
    # Si GET, afficher une page de confirmation
    return render(request, "accounts/logout_confirm.html")


def view_home(request):
    """Page d'accueil du site"""
    return render(request, "accounts/home.html")


class MyPasswordResetView(auth_views.PasswordResetView):
    """
    Vue personnalisée de réinitialisation de mot de passe
    Envoie un email avec un lien de réinitialisation
    """
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.txt"
    html_email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:verification_sent")
    
    def form_valid(self, form):
        """Afficher un message de succès après l'envoi de l'email"""
        messages.info(
            self.request,
            "Si un compte existe avec cet email, vous recevrez un lien de réinitialisation dans quelques instants."
        )
        return super().form_valid(form)