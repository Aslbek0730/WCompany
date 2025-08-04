from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order management
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel-order'),
    path('<int:order_id>/track/', views.track_order, name='track-order'),
    
    # Order status updates
    path('<int:order_id>/status-updates/', views.OrderStatusUpdateView.as_view(), name='status-updates'),
    
    # Order documents
    path('<int:order_id>/documents/', views.OrderDocumentView.as_view(), name='documents'),
    path('documents/<int:pk>/', views.OrderDocumentDetailView.as_view(), name='document-detail'),
    
    # Statistics
    path('statistics/', views.order_statistics, name='order-statistics'),
] 