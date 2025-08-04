from rest_framework import serializers
from .models import News, NewsCategory, Service, CompanyInfo, FAQ


class NewsCategorySerializer(serializers.ModelSerializer):
    """Serializer for news categories"""
    
    class Meta:
        model = NewsCategory
        fields = [
            'id', 'name', 'slug', 'description', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NewsSerializer(serializers.ModelSerializer):
    """Serializer for news model"""
    
    category = NewsCategorySerializer(read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'image',
            'category', 'status', 'author_name', 'created_at',
            'published_at', 'updated_at', 'meta_title', 'meta_description'
        ]
        read_only_fields = ['id', 'slug', 'author_name', 'created_at', 'published_at', 'updated_at']


class NewsCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating news"""
    
    class Meta:
        model = News
        fields = [
            'title', 'content', 'excerpt', 'image', 'category',
            'status', 'meta_title', 'meta_description'
        ]
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class NewsUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating news"""
    
    class Meta:
        model = News
        fields = [
            'title', 'content', 'excerpt', 'image', 'category',
            'status', 'meta_title', 'meta_description'
        ]


class NewsListSerializer(serializers.ModelSerializer):
    """Serializer for news list view"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'excerpt', 'image', 'category_name',
            'status', 'author_name', 'created_at', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'published_at']


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for service model"""
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'service_type', 'price', 'currency', 'icon', 'image',
            'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class ServiceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating services"""
    
    class Meta:
        model = Service
        fields = [
            'name', 'description', 'short_description', 'service_type',
            'price', 'currency', 'icon', 'image', 'is_active', 'order'
        ]


class ServiceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating services"""
    
    class Meta:
        model = Service
        fields = [
            'name', 'description', 'short_description', 'service_type',
            'price', 'currency', 'icon', 'image', 'is_active', 'order'
        ]


class CompanyInfoSerializer(serializers.ModelSerializer):
    """Serializer for company information"""
    
    class Meta:
        model = CompanyInfo
        fields = [
            'id', 'title', 'info_type', 'content', 'is_active',
            'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CompanyInfoCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating company information"""
    
    class Meta:
        model = CompanyInfo
        fields = [
            'title', 'info_type', 'content', 'is_active', 'order'
        ]


class CompanyInfoUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating company information"""
    
    class Meta:
        model = CompanyInfo
        fields = [
            'title', 'info_type', 'content', 'is_active', 'order'
        ]


class FAQSerializer(serializers.ModelSerializer):
    """Serializer for FAQ model"""
    
    class Meta:
        model = FAQ
        fields = [
            'id', 'question', 'answer', 'is_active', 'order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FAQCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating FAQ"""
    
    class Meta:
        model = FAQ
        fields = [
            'question', 'answer', 'is_active', 'order'
        ]


class FAQUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating FAQ"""
    
    class Meta:
        model = FAQ
        fields = [
            'question', 'answer', 'is_active', 'order'
        ]


class PublicNewsSerializer(serializers.ModelSerializer):
    """Public serializer for published news"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'image',
            'category_name', 'author_name', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'published_at']


class PublicServiceSerializer(serializers.ModelSerializer):
    """Public serializer for active services"""
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'service_type', 'price', 'currency', 'icon', 'image'
        ]
        read_only_fields = ['id', 'slug']


class PublicCompanyInfoSerializer(serializers.ModelSerializer):
    """Public serializer for active company information"""
    
    class Meta:
        model = CompanyInfo
        fields = [
            'id', 'title', 'info_type', 'content'
        ]
        read_only_fields = ['id']


class PublicFAQSerializer(serializers.ModelSerializer):
    """Public serializer for active FAQ"""
    
    class Meta:
        model = FAQ
        fields = [
            'id', 'question', 'answer'
        ]
        read_only_fields = ['id'] 