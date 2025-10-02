# stock/urls.py
from django.urls import path
from .views import *

app_name = 'stock'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('movements/', MovementListView.as_view(), name='movement_list'),
    path('movements/add/', MovementCreateView.as_view(), name='movement_create'),
    path('movements/<int:pk>/edit/', MovementUpdateView.as_view(), name='movement_update'),
    path('movements/<int:pk>/delete/', MovementDeleteView.as_view(), name='movement_delete'),
    path('movements/<int:pk>/', MovementDetailView.as_view(), name='movement_detail'),
    path("alerts/", alerts_view, name="alerts_list"),
    path('export/', MovementExportXLSXView.as_view(), name='export_xlsx'),
]
