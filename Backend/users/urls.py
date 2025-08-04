from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/passport/', views.PassportView.as_view(), name='passport'),
    
    # Documents
    path('documents/', views.UserDocumentView.as_view(), name='documents'),
    path('documents/<int:pk>/', views.UserDocumentDetailView.as_view(), name='document-detail'),
    
    # Verification
    path('verify/send-code/', views.send_verification_code, name='send-verification-code'),
    path('verify/confirm/', views.verify_code, name='verify-code'),
    
    # Password
    path('change-password/', views.change_password, name='change-password'),
] 