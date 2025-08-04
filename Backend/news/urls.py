from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Admin News Management
    path('admin/', views.NewsListView.as_view(), name='admin-news-list'),
    path('admin/<int:pk>/', views.NewsDetailView.as_view(), name='admin-news-detail'),
    path('admin/categories/', views.NewsCategoryListView.as_view(), name='admin-category-list'),
    path('admin/categories/<int:pk>/', views.NewsCategoryDetailView.as_view(), name='admin-category-detail'),
    
    # Public News
    path('public/', views.PublicNewsListView.as_view(), name='public-news-list'),
    path('public/<slug:slug>/', views.PublicNewsDetailView.as_view(), name='public-news-detail'),
    
    # Admin Service Management
    path('admin/services/', views.ServiceListView.as_view(), name='admin-service-list'),
    path('admin/services/<int:pk>/', views.ServiceDetailView.as_view(), name='admin-service-detail'),
    
    # Public Services
    path('public/services/', views.PublicServiceListView.as_view(), name='public-service-list'),
    path('public/services/<slug:slug>/', views.PublicServiceDetailView.as_view(), name='public-service-detail'),
    
    # Admin Company Info Management
    path('admin/company-info/', views.CompanyInfoListView.as_view(), name='admin-company-info-list'),
    path('admin/company-info/<int:pk>/', views.CompanyInfoDetailView.as_view(), name='admin-company-info-detail'),
    
    # Public Company Info
    path('public/company-info/', views.PublicCompanyInfoListView.as_view(), name='public-company-info-list'),
    path('public/company-info/<int:pk>/', views.PublicCompanyInfoDetailView.as_view(), name='public-company-info-detail'),
    
    # Admin FAQ Management
    path('admin/faq/', views.FAQListView.as_view(), name='admin-faq-list'),
    path('admin/faq/<int:pk>/', views.FAQDetailView.as_view(), name='admin-faq-detail'),
    
    # Public FAQ
    path('public/faq/', views.PublicFAQListView.as_view(), name='public-faq-list'),
    
    # Statistics and Dashboard
    path('admin/statistics/', views.news_statistics, name='news-statistics'),
    path('public/home-data/', views.public_home_data, name='public-home-data'),
] 