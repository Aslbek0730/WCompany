from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    # Support ticket management
    path('tickets/', views.SupportTicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.SupportTicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:ticket_id>/close/', views.close_ticket, name='close-ticket'),
    path('tickets/<int:ticket_id>/resolve/', views.resolve_ticket, name='resolve-ticket'),
    
    # Support messages
    path('tickets/<int:ticket_id>/messages/', views.SupportMessageListView.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.SupportMessageDetailView.as_view(), name='message-detail'),
    path('messages/<int:message_id>/read/', views.mark_message_read, name='mark-message-read'),
    
    # Support categories (admin only)
    path('categories/', views.SupportCategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.SupportCategoryDetailView.as_view(), name='category-detail'),
    
    # Support templates (admin only)
    path('templates/', views.SupportTemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', views.SupportTemplateDetailView.as_view(), name='template-detail'),
    
    # Statistics and search
    path('statistics/', views.support_statistics, name='support-statistics'),
    path('search/', views.search_tickets, name='search-tickets'),
] 