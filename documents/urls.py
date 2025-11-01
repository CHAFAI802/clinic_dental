from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('templates/', views.template_list, name='template_list'),
    path('templates/new/', views.create_template, name='create_template'),
    path('templates/<int:pk>/edit/', views.edit_template, name='edit_template'),
    path('templates/<int:pk>/delete/', views.delete_template, name='delete_template'),
    path('templates/<int:pk>/', views.document_preview, name='create_document'),
    path('upload_image/', views.upload_image, name='upload_image'),
]
