from django.urls import path
from .views import *
from .import views
from django.views.generic import CreateView, UpdateView, DeleteView

app_name = "billing"

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path("<int:pk>/", views.invoice_detail, name="invoice_detail"),
    path("add/", views.invoice_create, name="invoice_create"),
    path("<int:pk>/edit/", views.invoice_update, name="invoice_update"),
    path("<int:pk>/delete/", views.invoice_delete, name="invoice_delete"),
    path("<int:pk>/pdf/", views.invoice_pdf, name="invoice_pdf"),  # ➕ Génération PDF
    path('<int:invoice_id>/items/add/', InvoiceItemCreateView.as_view(), name='invoiceitem_create'),
    path('items/<int:pk>/edit/', InvoiceItemUpdateView.as_view(), name='invoiceitem_update'),
    path('items/<int:pk>/delete/', InvoiceItemDeleteView.as_view(), name='invoiceitem_delete'),
]
