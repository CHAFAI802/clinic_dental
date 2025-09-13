from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import MyPasswordResetView  


app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('',views.view_home,name='home'),
    path(
        "password_reset/",
        MyPasswordResetView.as_view(),
        name="password_reset",
    ),

    # page « lien envoyé »
    path(
        "verification-sent/",
        TemplateView.as_view(template_name="accounts/verification_sent.html"),
        name="verification_sent",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]