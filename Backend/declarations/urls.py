from django.urls import path
from . import views

app_name = 'declarations'

urlpatterns = [
    # Declaration management
    path('', views.DeclarationListView.as_view(), name='declaration-list'),
    path('<int:pk>/', views.DeclarationDetailView.as_view(), name='declaration-detail'),
    path('<int:declaration_id>/submit/', views.submit_declaration, name='submit-declaration'),
    path('<int:declaration_id>/approve/', views.approve_declaration, name='approve-declaration'),
    path('<int:declaration_id>/reject/', views.reject_declaration, name='reject-declaration'),
    path('<int:declaration_id>/pdf/', views.generate_pdf, name='generate-pdf'),
    
    # Declaration status updates
    path('<int:declaration_id>/status-updates/', views.DeclarationStatusUpdateView.as_view(), name='status-updates'),
    
    # Declaration documents
    path('<int:declaration_id>/documents/', views.DeclarationDocumentView.as_view(), name='documents'),
    path('documents/<int:pk>/', views.DeclarationDocumentDetailView.as_view(), name='document-detail'),
    
    # Statistics
    path('statistics/', views.declaration_statistics, name='declaration-statistics'),
] 