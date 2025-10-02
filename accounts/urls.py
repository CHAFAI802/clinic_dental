from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = "accounts"

urlpatterns = [
    # Pages principales
    path("", views.view_home, name="home"),
    path("register/", views.register, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("resend-activation/", views.resend_activation, name="resend_activation"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Réinitialisation de mot de passe
    path(
        "password-reset/",
        views.MyPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/sent/",
        TemplateView.as_view(template_name="accounts/verification_sent.html"),
        name="verification_sent",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
               success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]