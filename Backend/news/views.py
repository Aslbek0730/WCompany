from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from .models import News, NewsCategory, Service, CompanyInfo, FAQ
from .serializers import (
    NewsSerializer, NewsCreateSerializer, NewsUpdateSerializer, NewsListSerializer,
    NewsCategorySerializer, ServiceSerializer, ServiceCreateSerializer, ServiceUpdateSerializer,
    CompanyInfoSerializer, CompanyInfoCreateSerializer, CompanyInfoUpdateSerializer,
    FAQSerializer, FAQCreateSerializer, FAQUpdateSerializer,
    PublicNewsSerializer, PublicServiceSerializer, PublicCompanyInfoSerializer, PublicFAQSerializer
)


# News Views
class NewsListView(generics.ListCreateAPIView):
    """List and create news (admin only)"""
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return News.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewsCreateSerializer
        return NewsListSerializer


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete news (admin only)"""
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = News.objects.all()


class PublicNewsListView(generics.ListAPIView):
    """Public list of published news"""
    serializer_class = PublicNewsSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = News.objects.filter(status='published')
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset


class PublicNewsDetailView(generics.RetrieveAPIView):
    """Public news detail view"""
    serializer_class = PublicNewsSerializer
    permission_classes = [permissions.AllowAny]
    queryset = News.objects.filter(status='published')
    lookup_field = 'slug'


# News Category Views
class NewsCategoryListView(generics.ListCreateAPIView):
    """List and create news categories (admin only)"""
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = NewsCategory.objects.all()


class NewsCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete news categories (admin only)"""
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = NewsCategory.objects.all()


# Service Views
class ServiceListView(generics.ListCreateAPIView):
    """List and create services (admin only)"""
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return Service.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceCreateSerializer
        return ServiceSerializer


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete services (admin only)"""
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Service.objects.all()


class PublicServiceListView(generics.ListAPIView):
    """Public list of active services"""
    serializer_class = PublicServiceSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Service.objects.filter(is_active=True)


class PublicServiceDetailView(generics.RetrieveAPIView):
    """Public service detail view"""
    serializer_class = PublicServiceSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Service.objects.filter(is_active=True)
    lookup_field = 'slug'


# Company Info Views
class CompanyInfoListView(generics.ListCreateAPIView):
    """List and create company information (admin only)"""
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return CompanyInfo.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompanyInfoCreateSerializer
        return CompanyInfoSerializer


class CompanyInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete company information (admin only)"""
    serializer_class = CompanyInfoSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = CompanyInfo.objects.all()


class PublicCompanyInfoListView(generics.ListAPIView):
    """Public list of active company information"""
    serializer_class = PublicCompanyInfoSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CompanyInfo.objects.filter(is_active=True)


class PublicCompanyInfoDetailView(generics.RetrieveAPIView):
    """Public company information detail view"""
    serializer_class = PublicCompanyInfoSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CompanyInfo.objects.filter(is_active=True)


# FAQ Views
class FAQListView(generics.ListCreateAPIView):
    """List and create FAQ (admin only)"""
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return FAQ.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FAQCreateSerializer
        return FAQSerializer


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete FAQ (admin only)"""
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = FAQ.objects.all()


class PublicFAQListView(generics.ListAPIView):
    """Public list of active FAQ"""
    serializer_class = PublicFAQSerializer
    permission_classes = [permissions.AllowAny]
    queryset = FAQ.objects.filter(is_active=True)


# Statistics and Dashboard Views
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def news_statistics(request):
    """Get news statistics for admin dashboard"""
    total_news = News.objects.count()
    published_news = News.objects.filter(status='published').count()
    draft_news = News.objects.filter(status='draft').count()
    archived_news = News.objects.filter(status='archived').count()
    
    total_services = Service.objects.count()
    active_services = Service.objects.filter(is_active=True).count()
    
    total_faq = FAQ.objects.count()
    active_faq = FAQ.objects.filter(is_active=True).count()
    
    return Response({
        'news': {
            'total': total_news,
            'published': published_news,
            'draft': draft_news,
            'archived': archived_news,
        },
        'services': {
            'total': total_services,
            'active': active_services,
        },
        'faq': {
            'total': total_faq,
            'active': active_faq,
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_home_data(request):
    """Get public home page data"""
    latest_news = News.objects.filter(status='published').order_by('-published_at')[:6]
    active_services = Service.objects.filter(is_active=True).order_by('order')[:6]
    company_info = CompanyInfo.objects.filter(is_active=True).first()
    
    return Response({
        'latest_news': PublicNewsSerializer(latest_news, many=True).data,
        'services': PublicServiceSerializer(active_services, many=True).data,
        'company_info': PublicCompanyInfoSerializer(company_info).data if company_info else None,
    }, status=status.HTTP_200_OK)
