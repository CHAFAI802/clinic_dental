from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    #path("edit-clinic-info/", views.edit_clinic_info, name="edit_clinic_info"),
    path('parametres-cabinet/', views.clinic_info_update, name='clinic_info_update'),
    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),
    path("clinic-preview/", views.clinic_preview, name="clinic_preview"),
]


