
from django.urls import path
from .views import (
    BillingListView,
    BillingCreateView,
    BillingUpdateView,
    BillingDeleteView,
    BillingTogglePaidView,
    BillingDetailView,
    generate_billing_pdf,  # si tu veux le PDF
)

app_name = "billing"

urlpatterns = [
    path('', BillingListView.as_view(), name='billing_list'),
    path('<int:pk>/detail',BillingDetailView.as_view(), name='billing_detail'),
    path('add/', BillingCreateView.as_view(), name='billing_add'),
    path('<int:pk>/edit/', BillingUpdateView.as_view(), name='billing_edit'),
    path('<int:pk>/delete/', BillingDeleteView.as_view(), name='billing_delete'),
    path('<int:pk>/toggle-paid/', BillingTogglePaidView.as_view(), name='billing_toggle_paid'),
    path('<int:pk>/pdf/', generate_billing_pdf, name='billing_pdf'),  # optionnel
]
